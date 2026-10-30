# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 10/27/2026
# Description: Contains the views for the views app

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

#View to display voter records
class VoterListView(ListView):
    
    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        '''A method to filter the queryset'''
        # start with entire queryset
        voters = super().get_queryset()

        #Filters
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = voters.filter(party_affiliation=party)
                
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                voters = voters.filter(date_of_birth__year__gte=min_dob)
                
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(date_of_birth__year__lte=max_dob)
                
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)
                
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                voters = voters.filter(v20state=True)
                
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                voters = voters.filter(v21town=True)
                
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=True)
                
        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                voters = voters.filter(v22general=True)
                
        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                voters = voters.filter(v23town=True)
                
        return voters

    def get_context_data(self, **kwargs):
        '''Provide context variables for the template dropdowns and search state'''
        context = super().get_context_data(**kwargs)
        context['parties'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['years'] = Voter.objects.values_list('date_of_birth__year', flat=True).distinct().order_by('date_of_birth__year')
        context['request_get'] = self.request.GET
        return context

#A view to show a voter record
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

#A view to display graphs of the data
class VoterGraphsView(VoterListView):
    template_name = 'voter_analytics/graphs.html'
    
    def get_context_data(self, **kwargs):
        '''Create the context (in this case, graphs and charts) for the template'''
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        voter_count = len(voters)
        years = [v.date_of_birth.year for v in voters]
        year_counts = {}
        for y in years:
            year_counts[y] = year_counts.get(y, 0) + 1
        x_years = list(year_counts.keys())
        y_years = list(year_counts.values())
        fig1 = go.Bar(x=x_years, y=y_years)
        title_text1 = f"Voter Distribution by Year of Birth (n={voter_count})"
        graph_div_year = plotly.offline.plot({"data": [fig1], 
                                         "layout_title_text": title_text1,
                                         }, auto_open=False, output_type="div")
        context['graph_div_year'] = graph_div_year
        parties = [v.party_affiliation for v in voters]
        party_counts = {}
        for p in parties:
            party_counts[p] = party_counts.get(p, 0) + 1
        x_parties = list(party_counts.keys())
        y_parties = list(party_counts.values())
        fig2 = go.Pie(labels=x_parties, values=y_parties)
        title_text2 = f"Voter Distribution by Party Affiliation (n={voter_count})"
        graph_div_party = plotly.offline.plot({"data": [fig2], 
                                         "layout_title_text": title_text2,
                                         }, auto_open=False, output_type="div")
        context['graph_div_party'] = graph_div_party
        x_elections = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        y_elections = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]
        fig3 = go.Bar(x=x_elections, y=y_elections)
        title_text3 = f"Vote Count by Election (n={voter_count})"
        graph_div_elections = plotly.offline.plot({"data": [fig3], 
                                         "layout_title_text": title_text3,
                                         }, auto_open=False, output_type="div")
        context['graph_div_elections'] = graph_div_elections
        return context