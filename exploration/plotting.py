import datetime as dt
import plotly.graph_objects as go

class CandlePlot:
    def __init__(self, df, candles=True):
        self.df_plot = df.copy()
        self.candles = candles
        self.fig = None
        self.create_candle_fig()
        
    
    def add_time_str(self):
        self.df_plot['s_time'] = [dt.datetime.strftime(t, 's%y-%m-%d %H:%M') for t in self.df_plot['time']]
        
    
    def create_candle_fig(self):
        self.add_time_str()
        
        self.fig = go.Figure()
        
        if self.candles is True:
            self.fig.add_trace(go.Candlestick(
                x=self.df_plot['s_time'],
                open=self.df_plot['mid_o'],
                high=self.df_plot['mid_h'],
                low=self.df_plot['mid_l'],
                close=self.df_plot['mid_c'],
                line={'width': 1},
                opacity=1,
                increasing_fillcolor='#24a06b',
                decreasing_fillcolor='#cc2e3c',
                increasing_line_color='#2ec886',
                decreasing_line_color='#ff3a4c'
            ))
        
    
    def update_layout(self, width, height, nticks):
        self.fig.update_yaxes(
            gridcolor='#1f292f'
        )

        self.fig.update_xaxes(
            gridcolor='#1f292f',
            rangeslider={'visible': False},
            nticks=nticks
        )

        self.fig.update_layout(
            width=width,
            height=height,
            margin={'l': 10, 'r': 10, 'b': 20, 't': 20},
            paper_bgcolor='#010114',
            plot_bgcolor='#010114',
            font={'size': 10, 'color': '#e1e1e1'}
        )
        
    
    def add_traces(self, line_traces):
        for trace in line_traces:
            self.fig.add_trace(go.Scatter(
                x=self.df_plot['s_time'],
                y=self.df_plot[trace],
                line={'width': 2},
                line_shape='spline',
                name=trace
            ))
        
    
    def show_plot(self, width=1000, height=600, nticks=7, line_traces=[]):
        self.add_traces(line_traces)
        self.update_layout(width, height, nticks)
        self.fig.show()
        
        
        
    
     
        