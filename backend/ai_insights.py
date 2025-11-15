"""
AI Insights Manager for NATO PMP Analyzer
Provides advanced AI-powered analysis and recommendations
"""

from typing import List, Dict
import os
from openai import OpenAI


class AIInsightsManager:
    """Generates AI-powered insights and recommendations"""

    def __init__(self, api_key: str = None):
        """
        Initialize AI insights manager

        Args:
            api_key: OpenAI API key (if None, uses environment variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def is_configured(self) -> bool:
        """Check if OpenAI is configured"""
        return self.client is not None

    def generate_portfolio_insights(self, documents: List[Dict]) -> Dict[str, str]:
        """
        Generate comprehensive portfolio insights

        Args:
            documents: List of processed documents

        Returns:
            Dictionary with various insights
        """
        if not self.is_configured():
            return self._generate_fallback_insights(documents)

        # Prepare portfolio summary for AI
        summary = self._create_portfolio_summary(documents)

        try:
            # Generate insights using GPT
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert NATO project management analyst. Analyze project portfolios and provide strategic insights."},
                    {"role": "user", "content": f"""Analyze this NATO project portfolio and provide insights:

{summary}

Please provide:
1. Strategic Overview (2-3 sentences)
2. Key Trends Identified (bullet points)
3. Risk Assessment (critical findings)
4. Opportunities for Synergy (cross-project collaboration)
5. Recommendations (actionable items)

Format your response clearly with headers."""}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            insights_text = response.choices[0].message.content

            # Parse response into sections
            return self._parse_insights_response(insights_text)

        except Exception as e:
            print(f"Error generating AI insights: {str(e)}")
            return self._generate_fallback_insights(documents)

    def _create_portfolio_summary(self, documents: List[Dict]) -> str:
        """Create text summary of portfolio for AI analysis"""
        successful_docs = [d for d in documents if d.get('success')]

        summary_parts = []
        summary_parts.append(f"Total Projects: {len(successful_docs)}\n")

        for doc in successful_docs:
            metadata = doc.get('metadata', {})
            project_name = metadata.get('project_name', 'Unknown')
            status = metadata.get('status', 'GREEN')
            word_count = metadata.get('word_count', 0)
            stakeholders = len(metadata.get('stakeholders', []))
            budget = metadata.get('budget', [])

            summary_parts.append(f"""
Project: {project_name}
- Status: {status}
- Size: {word_count} words
- Stakeholders: {stakeholders}
- Budget Info: {', '.join(budget) if budget else 'Not specified'}
""")

        return '\n'.join(summary_parts)

    def _parse_insights_response(self, text: str) -> Dict[str, str]:
        """Parse AI response into structured insights"""
        sections = {
            'strategic_overview': '',
            'trends': '',
            'risks': '',
            'synergies': '',
            'recommendations': ''
        }

        current_section = None
        lines = text.split('\n')

        for line in lines:
            line_lower = line.lower()

            if 'strategic overview' in line_lower:
                current_section = 'strategic_overview'
            elif 'trends' in line_lower or 'trend' in line_lower:
                current_section = 'trends'
            elif 'risk' in line_lower:
                current_section = 'risks'
            elif 'synerg' in line_lower or 'collaboration' in line_lower:
                current_section = 'synergies'
            elif 'recommendation' in line_lower:
                current_section = 'recommendations'
            elif current_section and line.strip():
                sections[current_section] += line + '\n'

        return sections

    def _generate_fallback_insights(self, documents: List[Dict]) -> Dict[str, str]:
        """Generate basic insights without AI when API not available"""
        successful_docs = [d for d in documents if d.get('success')]
        red_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'RED'])
        amber_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'AMBER'])
        green_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'GREEN'])

        total_stakeholders = sum(len(d.get('metadata', {}).get('stakeholders', []))
                                for d in successful_docs)

        health_score = (green_count / max(len(successful_docs), 1)) * 100

        insights = {
            'strategic_overview': f"""Portfolio consists of {len(successful_docs)} projects with an overall
health score of {health_score:.1f}%. {'Immediate attention required for critical projects.' if red_count > 0 else 'Portfolio is generally healthy.'}""",

            'trends': f"""• {green_count} projects on track (GREEN status)
• {amber_count} projects showing warning signs (AMBER status)
• {red_count} projects at critical risk (RED status)
• Average stakeholder engagement: {total_stakeholders / max(len(successful_docs), 1):.1f} per project""",

            'risks': f"""• {red_count} project(s) require immediate intervention
• Resource allocation may need review for AMBER projects
• Stakeholder communication critical for at-risk projects""" if red_count > 0 or amber_count > 0 else "• No critical risks identified\n• Continue monitoring project progress",

            'synergies': f"""• {total_stakeholders} total stakeholders identified across portfolio
• Review projects for shared resources and collaboration opportunities
• Consider cross-project knowledge sharing initiatives""",

            'recommendations': f"""• Priority: Address {red_count} RED status project(s)
• Conduct detailed review of {amber_count} AMBER projects
• Maintain momentum on {green_count} successful projects
• Implement regular portfolio health monitoring
• Enhance stakeholder engagement across all projects"""
        }

        return insights

    def generate_project_comparison(self, project1: Dict, project2: Dict) -> str:
        """
        Compare two projects and identify similarities/differences

        Args:
            project1: First project dictionary
            project2: Second project dictionary

        Returns:
            Comparison analysis string
        """
        if not self.is_configured():
            return self._basic_project_comparison(project1, project2)

        meta1 = project1.get('metadata', {})
        meta2 = project2.get('metadata', {})

        prompt = f"""Compare these two NATO projects and identify:
1. Similarities (technology, stakeholders, objectives)
2. Differences (scope, status, approach)
3. Potential for collaboration or knowledge sharing

Project 1: {meta1.get('project_name', 'Unknown')}
- Status: {meta1.get('status', 'N/A')}
- Stakeholders: {len(meta1.get('stakeholders', []))}

Project 2: {meta2.get('project_name', 'Unknown')}
- Status: {meta2.get('status', 'N/A')}
- Stakeholders: {len(meta2.get('stakeholders', []))}

Provide a concise analysis (3-4 paragraphs)."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a NATO project management analyst specializing in project comparison and synergy identification."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except:
            return self._basic_project_comparison(project1, project2)

    def _basic_project_comparison(self, project1: Dict, project2: Dict) -> str:
        """Basic comparison without AI"""
        meta1 = project1.get('metadata', {})
        meta2 = project2.get('metadata', {})

        # Find shared stakeholders
        stakeholders1 = set(s.strip('_') for s in meta1.get('stakeholders', []))
        stakeholders2 = set(s.strip('_') for s in meta2.get('stakeholders', []))
        shared = stakeholders1.intersection(stakeholders2)

        comparison = f"""
**Project Comparison:**

**{meta1.get('project_name', 'Project 1')}** vs **{meta2.get('project_name', 'Project 2')}**

**Status Comparison:**
- Project 1: {meta1.get('status', 'N/A')}
- Project 2: {meta2.get('status', 'N/A')}

**Size Comparison:**
- Project 1: {meta1.get('word_count', 0):,} words
- Project 2: {meta2.get('word_count', 0):,} words

**Stakeholder Overlap:**
- Shared stakeholders: {len(shared)}
- Unique to Project 1: {len(stakeholders1 - stakeholders2)}
- Unique to Project 2: {len(stakeholders2 - stakeholders1)}

{"**Collaboration Opportunity:** " + str(len(shared)) + " shared stakeholders suggest potential for coordination." if shared else "**Limited Overlap:** Projects appear to have distinct stakeholder groups."}
"""

        return comparison

    def predict_project_risks(self, document: Dict) -> Dict[str, any]:
        """
        Predict potential risks for a project

        Args:
            document: Project document dictionary

        Returns:
            Risk prediction dictionary
        """
        metadata = document.get('metadata', {})
        status = metadata.get('status', 'GREEN')
        word_count = metadata.get('word_count', 0)
        stakeholder_count = len(metadata.get('stakeholders', []))

        # Simple heuristic-based risk assessment
        risk_factors = []
        risk_score = 0

        if status == 'RED':
            risk_factors.append("Critical status indicator")
            risk_score += 40
        elif status == 'AMBER':
            risk_factors.append("Warning status indicator")
            risk_score += 20

        if word_count < 500:
            risk_factors.append("Insufficient documentation")
            risk_score += 15

        if stakeholder_count < 2:
            risk_factors.append("Limited stakeholder engagement")
            risk_score += 15

        if not metadata.get('budget'):
            risk_factors.append("No budget information")
            risk_score += 10

        if not metadata.get('dates'):
            risk_factors.append("No timeline information")
            risk_score += 10

        # Determine risk level
        if risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 25:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendations': self._generate_risk_recommendations(risk_factors)
        }

    def _generate_risk_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate recommendations based on risk factors"""
        recommendations = []

        if "Critical status indicator" in risk_factors:
            recommendations.append("Immediate management intervention required")
            recommendations.append("Conduct emergency project review")

        if "Warning status indicator" in risk_factors:
            recommendations.append("Schedule detailed project assessment")

        if "Insufficient documentation" in risk_factors:
            recommendations.append("Enhance project documentation")

        if "Limited stakeholder engagement" in risk_factors:
            recommendations.append("Increase stakeholder communication and involvement")

        if "No budget information" in risk_factors:
            recommendations.append("Document and review budget allocation")

        if "No timeline information" in risk_factors:
            recommendations.append("Establish clear project milestones and deadlines")

        return recommendations

    def generate_executive_summary(self, documents: List[Dict]) -> str:
        """
        Generate executive summary of portfolio

        Args:
            documents: List of processed documents

        Returns:
            Executive summary text
        """
        successful_docs = [d for d in documents if d.get('success')]
        red_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'RED'])
        amber_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'AMBER'])
        green_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'GREEN'])

        health_score = (green_count / max(len(successful_docs), 1)) * 100

        summary = f"""
## Executive Summary

**Portfolio Overview:**
The NATO project portfolio currently contains {len(successful_docs)} active project(s) with an overall
health score of {health_score:.1f}%.

**Status Distribution:**
- 🟢 **{green_count} project(s)** are on track and meeting objectives
- 🟡 **{amber_count} project(s)** require monitoring and may need support
- 🔴 **{red_count} project(s)** are at critical risk and require immediate attention

**Key Metrics:**
- Total stakeholders engaged: {sum(len(d.get('metadata', {}).get('stakeholders', [])) for d in successful_docs)}
- Average project size: {sum(d.get('metadata', {}).get('word_count', 0) for d in successful_docs) / max(len(successful_docs), 1):.0f} words
- Projects with budget information: {len([d for d in successful_docs if d.get('metadata', {}).get('budget')])}

**Management Priorities:**
"""

        if red_count > 0:
            summary += f"1. **CRITICAL:** {red_count} RED project(s) need immediate intervention\n"
        if amber_count > 0:
            summary += f"2. **MONITOR:** {amber_count} AMBER project(s) require close monitoring\n"

        summary += "3. **SUSTAIN:** Maintain momentum on successful projects\n"
        summary += "4. **OPTIMIZE:** Identify cross-project synergies and collaboration opportunities\n"

        return summary
