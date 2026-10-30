from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Result
import plotly
import plotly.graph_objs as go
 
class ResultsListView(ListView):
    '''View to display marathon results'''
 
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
 
    def get_queryset(self):
        results = super().get_queryset().order_by('place_overall')
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city:
                results = results.filter(city=city)
                
        return results

class ResultDetailView(DetailView):
    '''view to show details for one result'''
 
    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'
 
    def get_context_data(self, **kwargs) :
        '''send context to the template'''
        context = super().get_context_data(**kwargs)
        r = context['r']
 
        x = ['first half', 'second half']
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        y = [first_half_seconds , second_half_seconds]
        fig = go.Pie(labels=x, values=y) 
        title_text = f"Half Marathon Splits"
        graph_div_splits = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_splits'] = graph_div_splits
        x= [f'Runners Passed by {r.first_name}', f'Runners who Passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        
        fig = go.Bar(x=x, y=y)
        title_text = f"Runners Passed/Passed By"
        graph_div_passed = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",               
                                         ) 
        context['graph_div_passed'] = graph_div_passed