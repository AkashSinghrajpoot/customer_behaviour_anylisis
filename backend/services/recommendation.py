"""
Recommendation engine for customer actions and strategies.

Generates human-readable, business-driven recommendations based on
customer metrics, engagement scores, and prediction results.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generates business recommendations for customer engagement."""

    @staticmethod
    def generate_recommendations(
        customer_data: Dict[str, Any],
        prediction_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive recommendations for a customer.

        Args:
            customer_data: Processed customer data with metrics
            prediction_results: ML prediction results

        Returns:
            Dictionary containing recommendations and reasoning
        """
        logger.info("Generating recommendations for customer")

        engagement_score = customer_data.get('engagement_score', 0)
        relationship_score = customer_data.get('relationship_score', 0)
        subscription_prob = prediction_results.get('subscription_probability', 0)
        customer_segment = customer_data.get('customer_segment', 'Unknown')
        spending_efficiency = customer_data.get('spending_efficiency', 0)
        balance_util = customer_data.get('balance_utilization', 0)

        # Generate primary recommendation
        primary_action = RecommendationEngine._determine_primary_action(
            engagement_score, relationship_score, subscription_prob, spending_efficiency
        )

        # Generate secondary actions
        secondary_actions = RecommendationEngine._generate_secondary_actions(
            engagement_score, relationship_score, spending_efficiency, balance_util
        )

        # Generate priority actions
        priority = RecommendationEngine._calculate_priority(
            engagement_score, subscription_prob, customer_segment
        )

        recommendations = {
            'primary_action': primary_action,
            'secondary_actions': secondary_actions,
            'priority_level': priority,
            'reasoning': RecommendationEngine._generate_reasoning(
                engagement_score, relationship_score, subscription_prob
            ),
            'next_steps': RecommendationEngine._generate_next_steps(
                primary_action, secondary_actions, customer_segment
            )
        }

        logger.info(f"Recommendations generated: {primary_action}")
        return recommendations

    @staticmethod
    def _determine_primary_action(
        engagement: float,
        relationship: float,
        subscription_prob: float,
        spending_eff: float
    ) -> str:
        """
        Determine the primary action for customer engagement.

        Args:
            engagement: Engagement score (0-100)
            relationship: Relationship score (0-100)
            subscription_prob: Subscription probability (0-100)
            spending_eff: Spending efficiency (0-1)

        Returns:
            Primary action recommendation
        """
        # High balance + high subscription probability
        if subscription_prob >= 75 and relationship >= 70:
            return "Offer Premium Banking Services"

        # Low engagement requiring relationship building
        if engagement < 40 and relationship >= 50:
            return "Initiate Personalized Relationship Follow-up"

        # High campaign frequency but low conversion
        if spending_eff > 0.8 and subscription_prob < 50:
            return "Reduce Outreach Frequency"

        # Growth opportunity
        if engagement >= 60 and subscription_prob >= 50:
            return "Cross-sell High-Value Financial Products"

        # At-risk customer
        if engagement < 50 and relationship < 50:
            return "Launch Retention Campaign"

        # Default recommendation
        return "Continue Standard Engagement"

    @staticmethod
    def _generate_secondary_actions(
        engagement: float,
        relationship: float,
        spending_eff: float,
        balance_util: float
    ) -> List[str]:
        """Generate secondary action recommendations."""
        actions = []

        # Engagement-based actions
        if engagement >= 80:
            actions.append("Consider loyalty program enrollment")
        elif engagement < 40:
            actions.append("Personalize communication preferences")

        # Relationship-based actions
        if relationship >= 75:
            actions.append("Offer dedicated account manager")
        elif relationship < 40:
            actions.append("Schedule financial planning consultation")

        # Balance actions
        if balance_util > 0.8:
            actions.append("Review credit limit increase opportunity")
        elif balance_util < 0.2:
            actions.append("Educate on credit utilization benefits")

        # Spending efficiency actions
        if spending_eff > 0.9:
            actions.append("Provide payment automation options")

        return actions

    @staticmethod
    def _calculate_priority(
        engagement: float,
        subscription_prob: float,
        segment: str
    ) -> str:
        """
        Calculate engagement priority level.

        Args:
            engagement: Engagement score
            subscription_prob: Subscription probability
            segment: Customer segment

        Returns:
            Priority level (Critical, High, Medium, Low)
        """
        if engagement >= 80 and subscription_prob >= 70:
            return "Critical"
        elif engagement >= 60 or subscription_prob >= 60:
            return "High"
        elif engagement >= 40 or subscription_prob >= 40:
            return "Medium"
        else:
            return "Low"

    @staticmethod
    def _generate_reasoning(
        engagement: float,
        relationship: float,
        subscription_prob: float
    ) -> str:
        """Generate human-readable reasoning for recommendations."""
        reasons = []

        if engagement >= 70:
            reasons.append("Strong engagement patterns detected")
        elif engagement < 40:
            reasons.append("Low engagement requires attention")

        if relationship >= 70:
            reasons.append("Positive relationship indicators")
        elif relationship < 40:
            reasons.append("Relationship building needed")

        if subscription_prob >= 70:
            reasons.append("High likelihood of subscription conversion")
        elif subscription_prob < 40:
            reasons.append("Conversion probability is low")

        return " | ".join(reasons) if reasons else "Customer profile under review"

    @staticmethod
    def _generate_next_steps(
        primary_action: str,
        secondary_actions: List[str],
        segment: str
    ) -> Dict[str, Any]:
        """Generate specific next steps for implementation."""
        action_templates = {
            "Offer Premium Banking Services": {
                "timeline": "Immediate (within 48 hours)",
                "channel": "Email + Phone",
                "message": "Exclusive premium banking offer for valued customers"
            },
            "Initiate Personalized Relationship Follow-up": {
                "timeline": "Within 1 week",
                "channel": "Personal outreach",
                "message": "Schedule relationship review call"
            },
            "Reduce Outreach Frequency": {
                "timeline": "Immediate",
                "channel": "System configuration",
                "message": "Lower contact frequency, increase personalization"
            },
            "Cross-sell High-Value Financial Products": {
                "timeline": "Within 2 weeks",
                "channel": "Multi-channel",
                "message": "Present tailored financial products"
            },
            "Launch Retention Campaign": {
                "timeline": "Immediate",
                "channel": "All available channels",
                "message": "Customer retention and re-engagement campaign"
            }
        }

        template = action_templates.get(primary_action, {
            "timeline": "Within 1 month",
            "channel": "Standard",
            "message": "Continue engagement strategy"
        })

        return {
            "immediate": f"Execute: {template['message']}",
            "timeline": template['timeline'],
            "preferred_channel": template['channel'],
            "segment_note": f"Priority handling for {segment} segment customers"
        }
