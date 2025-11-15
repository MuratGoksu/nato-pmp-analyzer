"""
Timeline Manager for NATO PMP Analyzer
Creates Gantt charts and timeline visualizations
"""

import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import re


class TimelineManager:
    """Manages timeline and Gantt chart visualizations"""

    def __init__(self):
        self.color_map = {
            'RED': '#dc3545',
            'AMBER': '#ffc107',
            'GREEN': '#28a745',
            'UNKNOWN': '#6c757d'
        }

    def extract_timeline_data(self, documents: list) -> list:
        """
        Extract timeline data from documents

        Args:
            documents: List of processed documents

        Returns:
            List of timeline events
        """
        timeline_data = []

        for doc in documents:
            if not doc.get('success'):
                continue

            metadata = doc.get('metadata', {})
            project_name = metadata.get('project_name', doc.get('file_name', 'Unknown'))
            dates = metadata.get('dates', [])
            status = metadata.get('status', 'GREEN')

            # Try to extract dates and create timeline entries
            if dates:
                # Parse dates and find earliest and latest
                parsed_dates = []
                for date_str in dates:
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        parsed_dates.append(parsed_date)

                if len(parsed_dates) >= 2:
                    # Use earliest and latest dates
                    start_date = min(parsed_dates)
                    end_date = max(parsed_dates)
                elif len(parsed_dates) == 1:
                    # If only one date, assume 6-month project
                    start_date = parsed_dates[0]
                    end_date = start_date + timedelta(days=180)
                else:
                    continue

                timeline_data.append({
                    'Task': project_name[:40],  # Truncate long names
                    'Start': start_date,
                    'Finish': end_date,
                    'Status': status,
                    'Resource': f"Status: {status}"
                })
            else:
                # No dates found - create placeholder with current date
                start_date = datetime.now()
                end_date = start_date + timedelta(days=180)

                timeline_data.append({
                    'Task': f"{project_name[:40]} (estimated)",
                    'Start': start_date,
                    'Finish': end_date,
                    'Status': status,
                    'Resource': f"Status: {status} (no dates found)"
                })

        return timeline_data

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string into datetime object

        Args:
            date_str: Date string in various formats

        Returns:
            datetime object or None
        """
        # Try different date formats
        formats = [
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%m/%d/%Y',
            '%B %d, %Y',
            '%d %B %Y',
            '%b %d, %Y',
            '%Y/%m/%d'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue

        # Try to extract year and create approximate date
        year_match = re.search(r'\b(20\d{2})\b', date_str)
        if year_match:
            year = int(year_match.group(1))
            return datetime(year, 1, 1)

        return None

    def create_gantt_chart(self, documents: list) -> go.Figure:
        """
        Create interactive Gantt chart

        Args:
            documents: List of processed documents

        Returns:
            Plotly figure object
        """
        timeline_data = self.extract_timeline_data(documents)

        if not timeline_data:
            # Return empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="No timeline data available. Upload documents with date information.",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="Project Timeline",
                height=400
            )
            return fig

        # Convert to DataFrame
        df = pd.DataFrame(timeline_data)

        # Create figure using plotly graph objects for more control
        fig = go.Figure()

        # Sort by start date
        df = df.sort_values('Start')

        # Add a bar for each project
        for idx, row in df.iterrows():
            duration = (row['Finish'] - row['Start']).days

            fig.add_trace(go.Bar(
                x=[duration],
                y=[row['Task']],
                orientation='h',
                base=row['Start'],
                marker=dict(
                    color=self.color_map.get(row['Status'], '#6c757d'),
                    line=dict(color='white', width=1)
                ),
                name=row['Status'],
                showlegend=False,
                hovertemplate=(
                    f"<b>{row['Task']}</b><br>" +
                    f"Start: {row['Start'].strftime('%Y-%m-%d')}<br>" +
                    f"End: {row['Finish'].strftime('%Y-%m-%d')}<br>" +
                    f"{row['Resource']}<br>" +
                    f"Duration: {duration} days<br>" +
                    "<extra></extra>"
                )
            ))

        # Update layout
        fig.update_layout(
            title=dict(
                text='Project Timeline (Gantt Chart)',
                font=dict(size=20)
            ),
            xaxis=dict(
                title='Date',
                type='date',
                tickformat='%Y-%m-%d'
            ),
            yaxis=dict(
                title='Projects',
                autorange='reversed'  # Top to bottom
            ),
            height=max(400, len(timeline_data) * 50),  # Dynamic height
            hovermode='closest',
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        return fig

    def create_timeline_chart(self, documents: list) -> go.Figure:
        """
        Create timeline scatter chart showing project milestones

        Args:
            documents: List of processed documents

        Returns:
            Plotly figure object
        """
        timeline_data = self.extract_timeline_data(documents)

        if not timeline_data:
            fig = go.Figure()
            fig.add_annotation(
                text="No timeline data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False
            )
            return fig

        # Create traces for start and end dates
        start_dates = []
        end_dates = []
        project_names = []
        statuses = []

        for item in timeline_data:
            project_names.append(item['Task'])
            start_dates.append(item['Start'])
            end_dates.append(item['Finish'])
            statuses.append(item['Status'])

        fig = go.Figure()

        # Add start markers
        fig.add_trace(go.Scatter(
            x=start_dates,
            y=project_names,
            mode='markers',
            name='Start Date',
            marker=dict(
                symbol='circle',
                size=12,
                color='green',
                line=dict(color='darkgreen', width=2)
            ),
            hovertemplate='<b>%{y}</b><br>Start: %{x}<extra></extra>'
        ))

        # Add end markers
        fig.add_trace(go.Scatter(
            x=end_dates,
            y=project_names,
            mode='markers',
            name='End Date',
            marker=dict(
                symbol='square',
                size=12,
                color='red',
                line=dict(color='darkred', width=2)
            ),
            hovertemplate='<b>%{y}</b><br>End: %{x}<extra></extra>'
        ))

        # Add connecting lines
        for i in range(len(project_names)):
            fig.add_trace(go.Scatter(
                x=[start_dates[i], end_dates[i]],
                y=[project_names[i], project_names[i]],
                mode='lines',
                line=dict(
                    color=self.color_map.get(statuses[i], '#6c757d'),
                    width=3
                ),
                showlegend=False,
                hoverinfo='skip'
            ))

        fig.update_layout(
            title='Project Timeline Overview',
            xaxis_title='Date',
            yaxis_title='Projects',
            height=max(400, len(project_names) * 40),
            hovermode='closest',
            plot_bgcolor='white',
            showlegend=True
        )

        return fig

    def create_milestone_chart(self, documents: list) -> go.Figure:
        """
        Create milestone chart showing all project dates

        Args:
            documents: List of processed documents

        Returns:
            Plotly figure object
        """
        milestones = []

        for doc in documents:
            if not doc.get('success'):
                continue

            metadata = doc.get('metadata', {})
            project_name = metadata.get('project_name', doc.get('file_name', 'Unknown'))
            dates = metadata.get('dates', [])
            status = metadata.get('status', 'GREEN')

            for date_str in dates:
                parsed_date = self._parse_date(date_str)
                if parsed_date:
                    milestones.append({
                        'Project': project_name[:30],
                        'Date': parsed_date,
                        'Status': status,
                        'Original': date_str
                    })

        if not milestones:
            fig = go.Figure()
            fig.add_annotation(
                text="No milestone data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False
            )
            return fig

        # Sort by date
        milestones.sort(key=lambda x: x['Date'])

        # Create scatter plot
        fig = go.Figure()

        # Group by status
        for status in ['RED', 'AMBER', 'GREEN']:
            status_milestones = [m for m in milestones if m['Status'] == status]

            if status_milestones:
                fig.add_trace(go.Scatter(
                    x=[m['Date'] for m in status_milestones],
                    y=[m['Project'] for m in status_milestones],
                    mode='markers',
                    name=status,
                    marker=dict(
                        size=14,
                        color=self.color_map[status],
                        symbol='diamond',
                        line=dict(color='white', width=2)
                    ),
                    hovertemplate='<b>%{y}</b><br>Date: %{x}<br>Status: ' + status + '<extra></extra>'
                ))

        fig.update_layout(
            title='Project Milestones',
            xaxis_title='Date',
            yaxis_title='Project',
            height=600,
            hovermode='closest',
            plot_bgcolor='white',
            showlegend=True
        )

        return fig

    def get_timeline_statistics(self, documents: list) -> dict:
        """
        Calculate timeline statistics

        Args:
            documents: List of processed documents

        Returns:
            Dictionary with statistics
        """
        timeline_data = self.extract_timeline_data(documents)

        if not timeline_data:
            return {
                'total_projects': 0,
                'projects_with_dates': 0,
                'earliest_start': None,
                'latest_end': None,
                'average_duration_days': 0
            }

        durations = [(item['Finish'] - item['Start']).days for item in timeline_data]

        return {
            'total_projects': len(timeline_data),
            'projects_with_dates': len([d for d in documents if d.get('metadata', {}).get('dates')]),
            'earliest_start': min(item['Start'] for item in timeline_data),
            'latest_end': max(item['Finish'] for item in timeline_data),
            'average_duration_days': sum(durations) / len(durations) if durations else 0,
            'min_duration_days': min(durations) if durations else 0,
            'max_duration_days': max(durations) if durations else 0
        }
