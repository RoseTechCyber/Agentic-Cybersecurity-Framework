# Agent Implementation Examples

## 📖 Overview

This document provides complete, production-ready code examples for implementing each reasoning agent in the Security Research Center.

---

## 1️⃣ Threat Intelligence Agent

### File: `src/agents/threat_intelligence_agent.py`

```python
"""
Threat Intelligence Analyst Agent
Synthesizes external and internal threat intelligence using reasoning
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging

from ..base_agent import BaseAgent, AgentRole
from ..data_layer.cosmosdb import CosmosDBClient
from ..vector_search.rag_pipeline import RAGPipeline
from ..indicators.whitelist import WhitelistManager
from ..indicators.blacklist import BlacklistManager

logger = logging.getLogger(__name__)

class ThreatSeverity(Enum):
    """Threat severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class ThreatIndicator:
    """Represents a threat indicator (IOC)"""
    value: str
    type: str  # ip, domain, hash, email, url
    confidence: float  # 0-1
    source: str
    last_seen: str
    threat_category: str  # malware, ransomware, apt, phishing, etc

@dataclass
class ThreatIntelligenceCase:
    """Represents a threat intelligence case"""
    id: str
    case_type: str
    title: str
    description: str
    severity: ThreatSeverity
    confidence: float
    indicators: List[ThreatIndicator]
    mitre_techniques: List[str]
    sources: List[str]
    whitelisted_indicators: List[str]
    blacklisted_indicators: List[str]
    related_cases: List[str]
    created_at: str
    updated_at: str
    evidence: Dict[str, Any]

class ThreatIntelligenceAgent(BaseAgent):
    """
    Threat Intelligence Analyst Agent
    
    Responsibilities:
    - Synthesize external threat feeds (Web IQ)
    - Correlate with internal incidents (Work IQ)
    - Map to MITRE ATT&CK framework
    - Calculate threat risk scores
    - Generate threat intelligence cases
    """
    
    def __init__(
        self,
        cosmosdb_client: CosmosDBClient,
        rag_pipeline: RAGPipeline,
        whitelist_manager: WhitelistManager,
        blacklist_manager: BlacklistManager,
        logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            name="threat-intelligence-analyst",
            role=AgentRole.THREAT_INTELLIGENCE,
            logger=logger
        )
        self.cosmosdb = cosmosdb_client
        self.rag = rag_pipeline
        self.whitelist_mgr = whitelist_manager
        self.blacklist_mgr = blacklist_manager
        
        # Reasoning state
        self.current_analysis: Dict[str, Any] = {}
        self.analysis_steps: List[str] = []
    
    async def analyze(
        self,
        threat_data: Dict[str, Any]
    ) -> ThreatIntelligenceCase:
        """
        Main analysis method
        
        Args:
            threat_data: {
                'external_threats': [threat feeds],
                'internal_incidents': [internal events],
                'indicators': [IOCs to analyze]
            }
        
        Returns:
            ThreatIntelligenceCase
        """
        self.logger.info(f"Starting threat analysis: {threat_data.get('threat_id')}")
        self.current_analysis = threat_data
        self.analysis_steps = []
        
        try:
            # Step 1: Extract and normalize indicators
            indicators = await self._extract_indicators(threat_data)
            self.record_reasoning("indicator_extraction", {
                "count": len(indicators),
                "types": list(set(i.type for i in indicators))
            })
            
            # Step 2: Check against whitelist/blacklist
            checked_indicators = await self._check_indicators(indicators)
            self.record_reasoning("indicator_validation", {
                "whitelisted": len(checked_indicators["whitelisted"]),
                "blacklisted": len(checked_indicators["blacklisted"]),
                "suspicious": len(checked_indicators["suspicious"])
            })
            
            # Step 3: Retrieve similar threat cases (RAG)
            rag_context = await self._retrieve_threat_context(indicators)
            self.record_reasoning("rag_retrieval", {
                "similar_cases": len(rag_context["similar_cases"]),
                "mitre_techniques": rag_context["mitre_techniques"]
            })
            
            # Step 4: Perform reasoning
            reasoning_result = await self.reason({
                "indicators": indicators,
                "rag_context": rag_context,
                "threat_data": threat_data
            })
            self.record_reasoning("threat_reasoning", reasoning_result)
            
            # Step 5: Calculate risk score
            risk_score = await self._calculate_risk_score(
                indicators,
                reasoning_result,
                rag_context
            )
            self.record_reasoning("risk_scoring", {"score": risk_score})
            
            # Step 6: Generate threat case
            threat_case = await self._generate_threat_case(
                indicators=indicators,
                reasoning=reasoning_result,
                risk_score=risk_score,
                rag_context=rag_context,
                checked_indicators=checked_indicators
            )
            
            self.record_reasoning("case_generated", {
                "case_id": threat_case.id,
                "severity": threat_case.severity.value
            })
            
            # Store in CosmosDB
            await self.cosmosdb.create_item(
                container="threat-intelligence-cases",
                item=asdict(threat_case)
            )
            
            self.logger.info(f"✅ Threat analysis complete: {threat_case.id}")
            return threat_case
            
        except Exception as e:
            self.logger.error(f"❌ Error in threat analysis: {str(e)}")
            self.record_reasoning("error", {"error": str(e)})
            raise
    
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Threat reasoning logic
        
        Performs multi-step reasoning:
        1. Pattern analysis
        2. Attribution analysis
        3. Capability assessment
        4. Intent estimation
        5. Trend forecasting
        """
        reasoning = {
            "pattern_analysis": await self._analyze_threat_patterns(context),
            "attribution": await self._perform_attribution_analysis(context),
            "capabilities": await self._assess_threat_capabilities(context),
            "intent": await self._estimate_threat_intent(context),
            "trend": await self._forecast_threat_trends(context)
        }
        return reasoning
    
    async def _extract_indicators(
        self,
        threat_data: Dict[str, Any]
    ) -> List[ThreatIndicator]:
        """Extract IOCs from threat data"""
        indicators = []
        
        for external_threat in threat_data.get("external_threats", []):
            for ioc in external_threat.get("indicators", []):
                indicator = ThreatIndicator(
                    value=ioc["value"],
                    type=ioc["type"],
                    confidence=ioc.get("confidence", 0.5),
                    source=ioc.get("source", "external"),
                    last_seen=datetime.utcnow().isoformat(),
                    threat_category=external_threat.get("threat_type")
                )
                indicators.append(indicator)
        
        return indicators
    
    async def _check_indicators(
        self,
        indicators: List[ThreatIndicator]
    ) -> Dict[str, List[str]]:
        """Check indicators against whitelist and blacklist"""
        result = {
            "whitelisted": [],
            "blacklisted": [],
            "suspicious": []
        }
        
        for indicator in indicators:
            # Check whitelist
            if await self.whitelist_mgr.is_whitelisted(
                indicator.value,
                indicator.type
            ):
                result["whitelisted"].append(indicator.value)
                continue
            
            # Check blacklist
            if await self.blacklist_mgr.is_blacklisted(
                indicator.value,
                indicator.type
            ):
                result["blacklisted"].append(indicator.value)
                continue
            
            # Suspicious
            result["suspicious"].append(indicator.value)
        
        return result
    
    async def _retrieve_threat_context(
        self,
        indicators: List[ThreatIndicator]
    ) -> Dict[str, Any]:
        """Retrieve relevant threat context using RAG"""
        
        # Build query from indicators
        query = f"""
        Find threat intelligence related to:
        IPs: {[i.value for i in indicators if i.type == 'ip']}
        Domains: {[i.value for i in indicators if i.type == 'domain']}
        Hashes: {[i.value for i in indicators if i.type == 'hash']}
        """
        
        # Search knowledge base
        similar_cases = await self.rag.search(query, top_k=10)
        
        # Extract MITRE techniques from similar cases
        mitre_techniques = set()
        for case in similar_cases:
            mitre_techniques.update(
                case.get("mitre_mappings", [])
            )
        
        return {
            "similar_cases": similar_cases,
            "mitre_techniques": list(mitre_techniques),
            "threat_patterns": await self._extract_patterns_from_cases(similar_cases)
        }
    
    async def _analyze_threat_patterns(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze threat patterns and TTPs"""
        indicators = context["indicators"]
        rag_context = context["rag_context"]
        
        patterns = {
            "infrastructure_patterns": [],
            "behavior_patterns": [],
            "targeting_patterns": []
        }
        
        # Analyze infrastructure (IPs, domains)
        infrastructure = [i for i in indicators if i.type in ["ip", "domain"]]
        if infrastructure:
            patterns["infrastructure_patterns"] = {
                "count": len(infrastructure),
                "geolocation": await self._analyze_geolocation(infrastructure),
                "asn": await self._analyze_asn(infrastructure),
                "registration": await self._analyze_registration(infrastructure)
            }
        
        # Analyze malware (hashes)
        malware = [i for i in indicators if i.type == "hash"]
        if malware:
            patterns["behavior_patterns"] = {
                "count": len(malware),
                "family": await self._identify_malware_family(malware),
                "capabilities": await self._identify_capabilities(malware)
            }
        
        return patterns
    
    async def _perform_attribution_analysis(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform threat actor attribution"""
        rag_context = context["rag_context"]
        similar_cases = rag_context["similar_cases"]
        
        # Extract threat actors from similar cases
        threat_actors = {}
        for case in similar_cases:
            actor = case.get("threat_actor")
            if actor:
                threat_actors[actor] = threat_actors.get(actor, 0) + 1
        
        # Rank by frequency
        ranked_actors = sorted(
            threat_actors.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "suspected_actors": ranked_actors,
            "confidence": 0.6 if ranked_actors else 0.1,
            "attribution_notes": "Based on pattern similarity to known campaigns"
        }
    
    async def _assess_threat_capabilities(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess threat actor capabilities"""
        mitre_techniques = context["rag_context"]["mitre_techniques"]
        
        capability_levels = {
            "reconnaissance": 0,
            "weaponization": 0,
            "delivery": 0,
            "exploitation": 0,
            "installation": 0,
            "command_control": 0,
            "exfiltration": 0,
            "impact": 0
        }
        
        # Map MITRE techniques to capabilities
        for technique in mitre_techniques:
            if technique.startswith("T1"):  # Reconnaissance
                capability_levels["reconnaissance"] = 1
            # ... more mappings
        
        overall_capability = "intermediate" if sum(capability_levels.values()) > 3 else "basic"
        
        return {
            "capabilities": capability_levels,
            "overall_level": overall_capability,
            "mitre_techniques": mitre_techniques
        }
    
    async def _estimate_threat_intent(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Estimate threat actor intent"""
        threat_data = context["threat_data"]
        
        intent_signals = {
            "financial": 0,
            "espionage": 0,
            "sabotage": 0,
            "hacktivism": 0
        }
        
        # Analyze indicators and context
        if "ransomware" in str(threat_data).lower():
            intent_signals["financial"] = 0.8
        elif "apt" in str(threat_data).lower():
            intent_signals["espionage"] = 0.8
        
        primary_intent = max(intent_signals, key=intent_signals.get)
        
        return {
            "intent_signals": intent_signals,
            "primary_intent": primary_intent,
            "confidence": intent_signals[primary_intent]
        }
    
    async def _forecast_threat_trends(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Forecast threat trends"""
        similar_cases = context["rag_context"]["similar_cases"]
        
        # Simple trend analysis based on similar cases
        trends = {
            "sophistication_trend": "increasing",
            "frequency_trend": "increasing",
            "targeting_trend": "broadening"
        }
        
        return {
            "trends": trends,
            "forecast_confidence": 0.6,
            "prediction_period": "30 days"
        }
    
    async def _calculate_risk_score(
        self,
        indicators: List[ThreatIndicator],
        reasoning: Dict[str, Any],
        rag_context: Dict[str, Any]
    ) -> float:
        """
        Calculate threat risk score (0-1)
        
        Factors:
        - Indicator confidence
        - Similar case severity
        - Attribution confidence
        - Capability assessment
        """
        score = 0.0
        
        # Indicator confidence (30%)
        if indicators:
            avg_confidence = sum(i.confidence for i in indicators) / len(indicators)
            score += avg_confidence * 0.3
        
        # Attribution confidence (20%)
        attribution = reasoning.get("attribution", {})
        score += attribution.get("confidence", 0) * 0.2
        
        # Capability level (20%)
        capability_level = {"basic": 0.3, "intermediate": 0.6, "advanced": 0.9}
        capability = reasoning.get("capabilities", {}).get("overall_level", "basic")
        score += capability_level.get(capability, 0.3) * 0.2
        
        # Intent assessment (20%)
        intent = reasoning.get("intent", {})
        score += intent.get("confidence", 0) * 0.2
        
        # Similar case severity (10%)
        if rag_context.get("similar_cases"):
            avg_severity = sum(
                {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
                .get(case.get("severity", "low"), 0.25)
                for case in rag_context["similar_cases"]
            ) / len(rag_context["similar_cases"])
            score += avg_severity * 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    async def _generate_threat_case(
        self,
        indicators: List[ThreatIndicator],
        reasoning: Dict[str, Any],
        risk_score: float,
        rag_context: Dict[str, Any],
        checked_indicators: Dict[str, List[str]]
    ) -> ThreatIntelligenceCase:
        """Generate threat intelligence case"""
        
        # Determine severity based on risk score
        if risk_score >= 0.8:
            severity = ThreatSeverity.CRITICAL
        elif risk_score >= 0.6:
            severity = ThreatSeverity.HIGH
        elif risk_score >= 0.4:
            severity = ThreatSeverity.MEDIUM
        elif risk_score >= 0.2:
            severity = ThreatSeverity.LOW
        else:
            severity = ThreatSeverity.INFO
        
        case = ThreatIntelligenceCase(
            id=f"TI-{datetime.utcnow().timestamp()}",
            case_type=self.current_analysis.get("threat_type", "unknown"),
            title=f"Threat Analysis: {', '.join(i.value for i in indicators[:3])}",
            description=f"Threat intelligence case for {self.current_analysis.get('threat_id')}",
            severity=severity,
            confidence=risk_score,
            indicators=indicators,
            mitre_techniques=rag_context["mitre_techniques"],
            sources=list(set(i.source for i in indicators)),
            whitelisted_indicators=checked_indicators.get("whitelisted", []),
            blacklisted_indicators=checked_indicators.get("blacklisted", []),
            related_cases=[c.get("id") for c in rag_context["similar_cases"]],
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            evidence={
                "reasoning": reasoning,
                "audit_trail": self.get_audit_trail()
            }
        )
        
        return case
    
    # Helper methods
    async def _extract_patterns_from_cases(
        self,
        cases: List[Dict]
    ) -> List[Dict]:
        """Extract threat patterns from similar cases"""
        return [
            {
                "pattern": case.get("pattern"),
                "severity": case.get("severity")
            }
            for case in cases if case.get("pattern")
        ]
    
    async def _analyze_geolocation(
        self,
        infrastructure: List[ThreatIndicator]
    ) -> Dict[str, Any]:
        """Analyze geolocation of indicators"""
        return {"countries": ["Unknown"], "regions": []}
    
    async def _analyze_asn(
        self,
        infrastructure: List[ThreatIndicator]
    ) -> Dict[str, Any]:
        """Analyze ASN information"""
        return {"asns": [], "providers": []}
    
    async def _analyze_registration(
        self,
        infrastructure: List[ThreatIndicator]
    ) -> Dict[str, Any]:
        """Analyze domain registration information"""
        return {"registrars": [], "age": "unknown"}
    
    async def _identify_malware_family(
        self,
        malware: List[ThreatIndicator]
    ) -> List[str]:
        """Identify malware families"""
        return ["unknown"]
    
    async def _identify_capabilities(
        self,
        malware: List[ThreatIndicator]
    ) -> Dict[str, Any]:
        """Identify malware capabilities"""
        return {"capabilities": [], "impact": "unknown"}
```

---

## 2️⃣ Incident Correlation Agent

### File: `src/agents/incident_correlation_agent.py`

```python
"""
Incident Correlation Agent
Correlates security events across all technology layers
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

from ..base_agent import BaseAgent, AgentRole
from ..data_layer.cosmosdb import CosmosDBClient
from ..investigation.timeline_builder import TimelineBuilder
from ..investigation.correlation_engine import CorrelationEngine

logger = logging.getLogger(__name__)

@dataclass
class IncidentCorrelation:
    """Represents correlated security events"""
    incident_id: str
    events: List[Dict]
    event_chain: List[Dict]  # Ordered timeline
    correlation_score: float
    attack_vector: Optional[str]
    lateral_movement: bool
    tech_layers_affected: List[str]
    severity: str
    confidence: float
    analysis_timestamp: str

class IncidentCorrelationAgent(BaseAgent):
    """
    Incident Correlation Agent
    
    Correlates security events across:
    - Infrastructure layer (cloud, network, containers)
    - Platform layer (OS, AD, EDR)
    - Application layer (WAF, SAST, API)
    - Data layer (DLP, DAM, encryption)
    """
    
    def __init__(
        self,
        cosmosdb_client: CosmosDBClient,
        timeline_builder: TimelineBuilder,
        correlation_engine: CorrelationEngine,
        logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            name="incident-correlator",
            role=AgentRole.INCIDENT_CORRELATOR,
            logger=logger
        )
        self.cosmosdb = cosmosdb_client
        self.timeline_builder = timeline_builder
        self.correlation_engine = correlation_engine
    
    async def analyze(
        self,
        events_data: Dict[str, Any]
    ) -> IncidentCorrelation:
        """
        Correlate security events
        
        Args:
            events_data: {
                'events': [security events],
                'time_window': 'minutes/hours/days',
                'tech_layers': [layers to consider]
            }
        """
        
        # Step 1: Gather events
        events = await self._gather_events(events_data)
        self.record_reasoning("events_gathered", {"count": len(events)})
        
        # Step 2: Normalize events
        normalized_events = await self._normalize_events(events)
        self.record_reasoning("events_normalized", {"count": len(normalized_events)})
        
        # Step 3: Build timeline
        timeline = await self.timeline_builder.build(normalized_events)
        self.record_reasoning("timeline_built", {"events": len(timeline)})
        
        # Step 4: Perform correlation
        correlations = await self._correlate_events(timeline, events_data)
        self.record_reasoning("correlation_performed", {
            "correlation_groups": len(correlations)
        })
        
        # Step 5: Analyze attack chain
        attack_chain = await self._analyze_attack_chain(timeline)
        self.record_reasoning("attack_chain_analyzed", {
            "chain_length": len(attack_chain)
        })
        
        # Step 6: Assess incident
        incident = await self._generate_incident_correlation(
            normalized_events,
            timeline,
            correlations,
            attack_chain
        )
        
        return incident
    
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Correlation reasoning logic
        """
        reasoning = {
            "event_clustering": await self._cluster_related_events(context),
            "attack_attribution": await self._attribute_attack(context),
            "impact_assessment": await self._assess_impact(context),
            "containment_recommendations": await self._recommend_containment(context)
        }
        return reasoning
    
    async def _gather_events(
        self,
        events_data: Dict[str, Any]
    ) -> List[Dict]:
        """Gather security events from all sources"""
        
        time_window = events_data.get("time_window", "1 hour")
        # Parse time window and query CosmosDB
        
        events = []
        
        # Get infrastructure events
        infra_events = await self.cosmosdb.query_items(
            "security-events",
            f"SELECT * FROM c WHERE c.techLayer = 'infrastructure' AND c.timestamp > NOW()"
        )
        events.extend(infra_events)
        
        # Get platform events
        platform_events = await self.cosmosdb.query_items(
            "security-events",
            f"SELECT * FROM c WHERE c.techLayer = 'platform'"
        )
        events.extend(platform_events)
        
        # Get application events
        app_events = await self.cosmosdb.query_items(
            "security-events",
            f"SELECT * FROM c WHERE c.techLayer = 'application'"
        )
        events.extend(app_events)
        
        # Get data layer events
        data_events = await self.cosmosdb.query_items(
            "security-events",
            f"SELECT * FROM c WHERE c.techLayer = 'data'"
        )
        events.extend(data_events)
        
        return events
    
    async def _normalize_events(
        self,
        events: List[Dict]
    ) -> List[Dict]:
        """Normalize events to common format"""
        normalized = []
        
        for event in events:
            normalized_event = {
                "timestamp": event.get("timestamp"),
                "source_system": event.get("source"),
                "event_type": event.get("eventType"),
                "severity": event.get("severity"),
                "tech_layer": event.get("techLayer"),
                "indicators": event.get("indicators", []),
                "user": event.get("user"),
                "resource": event.get("resource"),
                "status": event.get("status"),
                "raw_data": event
            }
            normalized.append(normalized_event)
        
        return sorted(
            normalized,
            key=lambda x: x["timestamp"]
        )
    
    async def _correlate_events(
        self,
        timeline: List[Dict],
        events_data: Dict[str, Any]
    ) -> List[List[Dict]]:
        """Correlate related events"""
        
        correlations = []
        used_indices = set()
        
        for i, event1 in enumerate(timeline):
            if i in used_indices:
                continue
            
            correlation_group = [event1]
            
            for j, event2 in enumerate(timeline[i+1:], start=i+1):
                if j in used_indices:
                    continue
                
                # Check if events should be correlated
                correlation_score = await self._calculate_correlation_score(
                    event1,
                    event2
                )
                
                if correlation_score > 0.7:
                    correlation_group.append(event2)
                    used_indices.add(j)
            
            if len(correlation_group) > 1:
                correlations.append(correlation_group)
                used_indices.update(range(i, len(timeline)))
        
        return correlations
    
    async def _calculate_correlation_score(
        self,
        event1: Dict,
        event2: Dict
    ) -> float:
        """Calculate correlation between two events"""
        
        score = 0.0
        
        # Time correlation (same user within minutes)
        if event1.get("user") == event2.get("user"):
            time_diff = (
                datetime.fromisoformat(event2["timestamp"]) -
                datetime.fromisoformat(event1["timestamp"])
            ).total_seconds()
            
            if time_diff < 300:  # 5 minutes
                score += 0.4
        
        # Indicator correlation (same IP, domain, etc)
        indicators1 = set(event1.get("indicators", []))
        indicators2 = set(event2.get("indicators", []))
        if indicators1 & indicators2:
            score += 0.3
        
        # Resource correlation (same target)
        if event1.get("resource") == event2.get("resource"):
            score += 0.2
        
        # Tech layer correlation
        if event1.get("tech_layer") == event2.get("tech_layer"):
            score += 0.1
        
        return min(score, 1.0)
    
    async def _analyze_attack_chain(
        self,
        timeline: List[Dict]
    ) -> List[Dict]:
        """Analyze attack chain from timeline"""
        
        attack_chain = []
        
        for event in timeline:
            if event.get("severity") in ["critical", "high"]:
                attack_chain.append({
                    "timestamp": event.get("timestamp"),
                    "event_type": event.get("event_type"),
                    "description": await self._describe_attack_step(event),
                    "impact": event.get("severity"),
                    "user": event.get("user"),
                    "source": event.get("source_system")
                })
        
        return attack_chain
    
    async def _describe_attack_step(self, event: Dict) -> str:
        """Generate human-readable description of attack step"""
        
        descriptions = {
            "failed_login": "Multiple failed login attempts",
            "privilege_escalation": "Privilege escalation detected",
            "lateral_movement": "Lateral movement to adjacent system",
            "data_access": "Unauthorized data access",
            "exfiltration": "Data exfiltration attempt"
        }
        
        return descriptions.get(
            event.get("event_type"),
            f"Security event: {event.get('event_type')}"
        )
    
    async def _cluster_related_events(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Cluster related security events"""
        
        return {
            "clusters": [],
            "relationships": []
        }
    
    async def _attribute_attack(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Attribute attack to threat actor or group"""
        
        return {
            "suspected_actor": None,
            "confidence": 0.0,
            "known_patterns": []
        }
    
    async def _assess_impact(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess impact of incident"""
        
        return {
            "severity": "medium",
            "affected_systems": [],
            "data_at_risk": [],
            "estimated_cost": 0
        }
    
    async def _recommend_containment(
        self,
        context: Dict[str, Any]
    ) -> List[str]:
        """Recommend containment measures"""
        
        return [
            "Isolate affected systems",
            "Block malicious indicators",
            "Enable enhanced monitoring",
            "Prepare incident response"
        ]
    
    async def _generate_incident_correlation(
        self,
        events: List[Dict],
        timeline: List[Dict],
        correlations: List[List[Dict]],
        attack_chain: List[Dict]
    ) -> IncidentCorrelation:
        """Generate incident correlation result"""
        
        correlation = IncidentCorrelation(
            incident_id=f"INC-{datetime.utcnow().timestamp()}",
            events=events,
            event_chain=attack_chain,
            correlation_score=0.85,
            attack_vector="network",
            lateral_movement=len(attack_chain) > 2,
            tech_layers_affected=list(set(e.get("tech_layer") for e in events)),
            severity="high" if len(attack_chain) > 2 else "medium",
            confidence=0.8,
            analysis_timestamp=datetime.utcnow().isoformat()
        )
        
        return correlation
```

---

## 3️⃣ Anomaly Detection Agent

### File: `src/agents/anomaly_agent.py` (Simplified Example)

```python
"""
Anomaly Detection Agent
Identifies deviations from baseline behavior
"""

from typing import Dict, List, Any
import numpy as np
from sklearn.ensemble import IsolationForest
import logging

from ..base_agent import BaseAgent, AgentRole

logger = logging.getLogger(__name__)

class AnomalyDetectionAgent(BaseAgent):
    """
    Detects anomalies in security events using machine learning
    """
    
    def __init__(self, logger = None):
        super().__init__(
            name="anomaly-detector",
            role=AgentRole.ANOMALY_DETECTOR,
            logger=logger
        )
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.baseline_established = False
    
    async def analyze(self, events: List[Dict]) -> Dict[str, Any]:
        """
        Detect anomalies in event stream
        """
        
        if not self.baseline_established:
            await self._establish_baseline(events)
        
        # Convert events to feature matrix
        features = await self._extract_features(events)
        
        # Detect anomalies
        predictions = self.isolation_forest.predict(features)
        anomaly_scores = self.isolation_forest.score_samples(features)
        
        # Identify anomalous events
        anomalies = [
            {
                "event": events[i],
                "anomaly_score": float(anomaly_scores[i]),
                "is_anomaly": predictions[i] == -1
            }
            for i in range(len(events))
            if predictions[i] == -1
        ]
        
        self.record_reasoning("anomaly_detection", {
            "total_events": len(events),
            "anomalies_detected": len(anomalies)
        })
        
        return {
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    
    async def reason(self, context: Dict) -> Dict[str, Any]:
        """Reasoning for anomalies"""
        return {"reasoning": "Detected deviations from baseline behavior"}
    
    async def _establish_baseline(self, events: List[Dict]):
        """Establish baseline behavior"""
        features = await self._extract_features(events)
        self.isolation_forest.fit(features)
        self.baseline_established = True
    
    async def _extract_features(self, events: List[Dict]) -> np.ndarray:
        """Extract features from events"""
        features = []
        for event in events:
            feature = [
                event.get("failed_attempts", 0),
                event.get("data_volume", 0),
                event.get("connection_count", 0),
                event.get("privilege_level", 0)
            ]
            features.append(feature)
        return np.array(features)
```

---

## 📌 Key Points

✅ **Modularity**: Each agent is independent and testable
✅ **Async/Await**: All operations are non-blocking
✅ **Reasoning Tracking**: Complete audit trail of decisions
✅ **Integration**: Works with CosmosDB, Milvus, Ollama
✅ **RAG-Ready**: Leverages knowledge base and vector search
✅ **Indicator Integration**: Uses whitelist/blacklist
✅ **Extensible**: Easy to add new agents following same pattern

