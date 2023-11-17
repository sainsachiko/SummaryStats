# %%
# Python imports
import os
import argparse
import plotly.express as px
import plotly
import pandas as pd
from itertools import count
from sys import stdout
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

# TreeVal imports
from fileparsing import ProjectStats
from master_list import master_list, data_for_plotting, subworkflows

DOCSTRING = f"""
{'-'*60}
TreeVal Project Summary Stats
{'-'*60}
Written by dp24 / DLBPointon
{'-'*60}

This script aims to pull actionable insights from data 
collected from the TreeVal pipeline. Although it could 
be generalised for others.

The main usecase will be the generation of data to ensure
the maximal efficient usage of HPC resources. We will also 
be adding support for the co2footprint plugin, to gain 
insights into the co2 impact of the pipeline.

Usage:
python3 src/treeval/scripts/ProjectStats.py ./treeval-summary-files/1-1-0/

"""
class Colours:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'


def get_command_args(args=None):
    parser = argparse.ArgumentParser(
        prog="ProjectStats (Python 3)", description=DOCSTRING, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("DIR", action="store", help="Directory of input Summary Files", type=str)
    
    parser.add_argument('-c', "--co2footprint", action="store", help="Directory of input CO2 Summary Files", type=str)

    parser.add_argument("-o", "--output", action="store", help="Output directory location", default="./StatGraphs/", type=str)

    parser.add_argument("-v", "--version", action="version", version="v1.0.0")
    
    parser.add_argument("--verbose", action="store", type=bool, default=False, help="Verbosity, do you want more information on the run?")

    options = parser.parse_args(args)
    return options


def subset_dataframe(data_df: pd.DataFrame, ticket: list):
    if len(ticket) > 0:
        df = data_df[data_df["Ticket"].isin(ticket)]
    else:
        df = data_df
    return df


def generate_genome_vs_runtime(data_df: pd.DataFrame):
    fig = px.scatter(data_df, x='Duration_(Hrs)', y='Fasta_(mb)',
                    height=400,
                    color='Clade', hover_data=['Unique_name'], trendline="ols",
                    trendline_options=dict(log_x=True), #trendline_scope="overall", #trendline_color_override="black",
                    title = 'Size of Genome (MB) against runtime (Hours) - ALL',
                    labels = { 'Fasta_(mb)' : 'Fasta Size (MB)',
                                'Duration_(Hrs)' : 'Runtime (Hours)',
                                'Clade' : 'Clade'})

    graph_ALL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    
    fig = px.scatter(data_df[data_df['Entry_Point'] == 'FULL'], x='Duration_(Hrs)', y='Fasta_(mb)',
                    height=400,
                    color='Clade', hover_data=['Unique_name'], trendline="ols",
                    trendline_options=dict(log_x=True), #trendline_scope="overall", #trendline_color_override="black",
                    title = 'Size of Genome (MB) against runtime (Hours) - FULL',
                    labels = { 'Fasta_(mb)' : 'Fasta Size (MB)',
                                'Duration_(Hrs)' : 'Runtime (Hours)',
                                'Clade' : 'Clade'})

    graph_FULL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'RAPID'], x='Duration_(Hrs)', y='Fasta_(mb)',
                    height=400,
                    color='Clade', hover_data=['Unique_name'], trendline="ols",
                    trendline_options=dict(log_x=True), #trendline_scope="overall", #trendline_color_override="black",
                    title = 'Size of Genome (MB) against runtime (Hours) - RAPID',
                    labels = { 'Fasta_(mb)' : 'Fasta Size (MB)',
                                'Duration_(Hrs)' : 'Runtime (Hours)',
                                'Clade' : 'Clade'})

    graph_RAPID = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_ALL, graph_FULL, graph_RAPID


def generate_clade_vs_runtime(data_df: pd.DataFrame):
    fig = px.scatter(data_df, y="Duration_(Hrs)", x="Clade", color="Clade",
                    title = 'Clade group against Runtime (Hours) - ALL',
                    height=400)
    graph_ALL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'FULL'], y="Duration_(Hrs)", x="Clade", color="Clade",
                    title = 'Clade group against Runtime (Hours) - FULL',
                    height=400)
    graph_FULL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'RAPID'], y="Duration_(Hrs)", x="Clade", color="Clade",
                    title = 'Clade group against Runtime (Hours) - RAPID',
                    height=400)
    graph_RAPID = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_ALL, graph_FULL, graph_RAPID


def generate_family_vs_runtime(data_df: pd.DataFrame):
    fig = px.scatter(data_df, y="Duration_(Hrs)", x="Prefix", color="Clade",
                    title = 'Clade group against Runtime (Hours) - ALL',
                    height=400)
    graph_ALL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'FULL'], y="Duration_(Hrs)", x="Prefix", color="Clade",
                    title = 'Clade group against Runtime (Hours) - FULL',
                    height=400)
    graph_FULL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'RAPID'], y="Duration_(Hrs)", x="Prefix", color="Clade",
                    title = 'Clade group against Runtime (Hours) - RAPID',
                    height=400)
    graph_RAPID = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_ALL, graph_FULL, graph_RAPID


def generate_longread_vs_runtime(data_df: pd.DataFrame):
    fig = px.scatter(data_df, x='Duration_(Hrs)', y='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    trendline="ols", trendline_options=dict(log_x=True),
                    trendline_scope="overall", trendline_color_override="black",
                    title = 'Total PacBio data against runtime (Hours) - ALL',
                    height=400)
    graph_ALL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'FULL'], x='Duration_(Hrs)', y='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    trendline="ols", trendline_options=dict(log_x=True),
                    trendline_scope="overall", trendline_color_override="black",
                    title = 'Total PacBio data against runtime (Hours) - FULL',
                    height=400)
    graph_FULL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'RAPID'], x='Duration_(Hrs)', y='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    trendline="ols", trendline_options=dict(log_x=True),
                    trendline_scope="overall", trendline_color_override="black",
                    title = 'Total PacBio data against runtime (Hours) - RAPID',
                    height=400)
    graph_RAPID = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_ALL, graph_FULL, graph_RAPID


def generate_hic_vs_runtime(data_df: pd.DataFrame):
    fig = px.scatter(data_df, x='Duration_(Hrs)', y='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    trendline_options=dict(log_x=True), trendline_scope="overall", trendline_color_override="black",
                    title = 'Total amount of CRAM data against runtime (Hours) - ALL',
                    height=400)
    graph_ALL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')


    fig = px.scatter(data_df[data_df['Entry_Point'] == 'FULL'], x='Duration_(Hrs)', y='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    trendline_options=dict(log_x=True), trendline_scope="overall", trendline_color_override="black",
                    title = 'Total amount of CRAM data against runtime (Hours) - FULL',
                    height=400)
    graph_FULL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    fig = px.scatter(data_df[data_df['Entry_Point'] == 'RAPID'], x='Duration_(Hrs)', y='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'], trendline="ols",
                    trendline_options=dict(log_x=True), trendline_scope="overall", trendline_color_override="black",
                    title = 'Total amount of CRAM data against runtime (Hours) - RAPID',
                    height=400)
    graph_RAPID = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_ALL, graph_FULL, graph_RAPID


def generate_3d_graphs(data_df: pd.DataFrame):
    fig = px.scatter_3d(data_df, x='Duration_(Hrs)', y='Fasta_(mb)', z='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    title = 'Size of Genome (MB) against runtime (Hours) - ALL',
                    height=1000)
    graph_ALL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')


    fig = px.scatter_3d(data_df[data_df['Entry_Point'] == 'FULL'], x='Duration_(Hrs)', y='Fasta_(mb)', z='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    title = 'Size of Genome (MB) against runtime (Hours) - FULL',
                    height=1000)
    graph_FULL = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')


    fig = px.scatter_3d(data_df[data_df['Entry_Point'] == 'RAPID'], x='Duration_(Hrs)', y='Fasta_(mb)', z='HiC_(TOTAL_GB)',
                    color='Clade', hover_data=['Prefix'],
                    title = 'Size of Genome (MB) against runtime (Hours) - RAPID',
                    height=1000)
    graph_RAPID = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_ALL, graph_FULL, graph_RAPID


def plot_average_mem_of_super_module(data_df: pd.DataFrame):
    colormap = plt.cm.bwr #or any other colormap
    plt.scatter(x = data_df['Unique_name'],
                y = data_df['HIC_MAPPING:CRAM_FILTER_ALIGN_BWAMEM2_FIXMATE_SORT-AVERAGE_P_MEM'],
                c = data_df['Fasta_(mb)'],
                cmap = colormap,
                norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.title("\n".join('HIC_MAPPING:CRAM_FILTER_ALIGN_BWAMEM2_FIXMATE_SORT-AVERAGE_P_MEM'.split(':')))
    plt.ylabel('Memory Utilisation (%)')
    plt.ylim(0,100)
    
    plt.savefig('HIC_super_module_average_mem.png')
    plt.clf()


def plot_average_cpu_of_super_module(data_df: pd.DataFrame):
    colormap = plt.cm.bwr #or any other colormap
    plt.scatter(x = data_df['Unique_name'],
                y = data_df['HIC_MAPPING:CRAM_FILTER_ALIGN_BWAMEM2_FIXMATE_SORT-AVERAGE_P_CPU'],
                c = data_df['Fasta_(mb)'],
                cmap = colormap,
                norm=matplotlib.colors.LogNorm())
    plt.colorbar()
    plt.title("\n".join('HIC_MAPPING:CRAM_FILTER_ALIGN_BWAMEM2_FIXMATE_SORT-AVERAGE_P_CPU'.split(':')))
    plt.ylabel('CPU Utilisation (%)')
    plt.ylim(0,1600)
    
    plt.savefig('HIC_super_module_average_cpu.png')
    plt.clf()


def generate_new_column_names(column_names):
    return ["CRAM_SUPER_MODULE" if i.split(':')[1].startswith('CRAM') else 'Unique_name' if i == 'Unique_name' else i.split(':')[1].split('-')[0] for i in column_names]

def plot_hic_boxplots(name: str, entry: str, data_df: pd.DataFrame, list_of_processes: list, debug: bool):

    if entry == 'ALL':
        pass
    else:
        data_df = data_df[data_df['Entry_Point'] == entry]

    # GENERATE LISTS FOR: 1) WHAT WE WANT IT CALLED, 2) WHAT FIRST DATASET IS CURRENTLY CALLED, 3) WHAT SECOND DATASET IS CURRENTLY CALLED
    processes       = ["CRAM_SUPER_MODULE" if i.split(':')[1].startswith('CRAM') else i.split(':')[1] for i in list_of_processes]
    processes_mem   = [i + "-AVERAGE_P_MEM" for i in list_of_processes]
    processes_peak  = [i + "-AVERAGE_PEAK_MEMORY" for i in list_of_processes]

    data_df_P_mem   = data_df[processes_mem].copy()
    data_df_P_mem.columns = generate_new_column_names(data_df_P_mem.columns)
    
    data_df_P_peak = data_df[processes_peak]
    data_df_P_peak.columns = generate_new_column_names(data_df_P_peak.columns)

    data_df_P_peak = data_df_P_peak.iloc[:, :] # Drops the unique name column otherwise plots per name and breaks max()
    max_values = data_df_P_peak.max()           # Get the max value per process 
    peak = pd.DataFrame(max_values)             # Make dataframe max()
    if debug:
        print(peak)                                 # For Debugging

    # Actually generates the graph
    sns.set(rc = {'figure.figsize':(25,25)})
    fig = sns.boxplot(data=data_df_P_mem, legend=False)
    fig.set(ylim=(0,110))
    ax2 = plt.twinx()
    ax2.set(ylim=(0,110))
    sns.scatterplot(data=peak, color='red', ax=ax2, legend=False)
    fig.set_xticks(processes)
    fig.set_xticklabels(processes, rotation=90, fontsize=6)
    fig.set_xlabel("Ticket", fontsize=6)
    plt.subplots_adjust(bottom=0.4)
    
    box = fig.get_figure()

    box.savefig(f"{name}_{entry}.png")
    plt.clf()                                   # Clear plot


def print_report(data_df: pd.DataFrame, empties: list):
    empty = ''
    stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')
    stdout.write(f"{Colours.BLUE}TreeVal{Colours.END}{Colours.RED}Project{Colours.END}.{Colours.GREEN}Summary{Colours.END} {Colours.YELLOW}Stats{Colours.END}!\n")
    stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')
    stdout.write(f"Total data points: {len(data_df)} \n")
    stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')
    stdout.write(f"Unique CLADE count:\n{data_df['Clade'].value_counts()}\n")
    stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')
    stdout.write(f"Run Type Count:\n{data_df['Entry_Point'].value_counts()}\n")
    stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')
    stdout.write(f"Ticket Type Count:\n{data_df['Ticket'].value_counts()}\n")
    stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')
    if len(empties) >= 1:
        [stdout.write(f"Empty Files!:\n{i}\n") for i in empties]
        stdout.write(f"{Colours.HEADER}-"*50 + f'\n {Colours.END}')

    breaker = f"{'-'*50}<br>"
    output_list = breaker + "TreeVal Project Summary Stats! <br>" + breaker + f"Total data points: {len(data_df)}<br>" + breaker + f"Unique CLADE count:\n{data_df['Clade'].value_counts()}<br>" + breaker + f"Run Type Count:\n{data_df['Entry_Point'].value_counts()}<br>" + breaker + f"Ticket Type Count:\n{data_df['Ticket'].value_counts()}<br>" + breaker
    return output_list


def main():
    options = get_command_args()
    if options.output[-1] != '/':
        outdir = options.output +'/'
    else:
        outdir = options.output

    list_of_lists = []
    empty_files = []

    for file in os.listdir(options.DIR):
        if os.stat(options.DIR + file).st_size == 0:
            empty_files.append(file)
            pass
        else:
            usable_data = options.DIR + file
            data = ProjectStats(usable_data)
            # print(data.execution.list_of_list) # | Execution log data
            # print(data.execution.headers)      # | Execution log headers
            data_list = [data.uniquename, data.header_block.entrypnt,
                                    data.header_block.version,data.header_block.duration.get('h'),
                                    data.header_block.genome_clade,data.id,
                                    data.fasta_mb,data.header_block.genome_ticket,
                                    data.pacbio_avg,data.cram_avg,
                                    data.header_block.pacbio_totaldata, data.header_block.cram_totaldata]
            data_and_execution = data_list + data.execution.list_of_list
            
            df_columns = [  'Unique_name', 'Entry_Point',
                            'Pipeline_Version', 'Duration_(Hrs)',
                            'Clade', 'Prefix',
                            'Fasta_(mb)', 'Ticket',
                            'Longread_(AVG_GB)', 'HiC_(AVG_GB)',
                            'Longread_(TOTAL_GB)', 'HiC_(TOTAL_GB)' ]

            df_columns += data.execution.headers # Adds execution log headers to the columns list

            list_of_lists.append(  
                                    data_and_execution
                                )

    header_df = pd.DataFrame(
                            list_of_lists,
                            columns = df_columns
                            )

    subset_df = subset_dataframe(header_df, ticket = [])

    #
    # THE PROCESS DATA IS IN LIST FORMAT ORGANISED AS: [ avg_cpu, avg_mem, avg_realtime, avg_pcpu, avg_pmem, avg_peak ]
    # FOR GRAPHING THIS NEEDS SPLITTING OUT INTO COLUMNS
    # DOING IT LIKE THIS IS NOT GOOD FOR PERFORMANCE HENCE THE WARNING FILTER ON LINE 17
    #
    for i in master_list:
        subset_df[[f'{i}-AVERAGE_CPU', f'{i}-AVERAGE_MEMORY', f'{i}-AVERAGE_REALTIME', f'{i}-AVERAGE_P_CPU', f'{i}-AVERAGE_P_MEM', f'{i}-AVERAGE_PEAK_MEMORY']] = pd.DataFrame(subset_df[f'{i}'].to_list(), index = subset_df.index)
        subset_df.replace('NA', np.nan, inplace=True)
        subset_df[[f'{i}-AVERAGE_CPU', f'{i}-AVERAGE_MEMORY', f'{i}-AVERAGE_REALTIME', f'{i}-AVERAGE_P_CPU', f'{i}-AVERAGE_P_MEM', f'{i}-AVERAGE_PEAK_MEMORY']].astype(float)

    subset_df.replace('NA', None)

    plot_average_mem_of_super_module(subset_df)

    plot_average_cpu_of_super_module(subset_df)

    for subworkflow_name in subworkflows:
        # Skipping gene alignment at the minute due to subworkflows inside the subworkflow causing over collapsing of data
        # In this case it will generate a graph containing data for RNA, CDS, CDNA and PEP which are themselves subworkflows
        # This also means that other sub-subworkflows will be effected
        if subworkflow_name not in ['GENE_ALIGNMENT', 'CUSTOM_DUMPSOFTWAREVERSIONS']:
            subworkflow_processes = [i + "" for i in master_list if i.startswith(subworkflow_name)]
            for x in ['FULL', 'RAPID', 'ALL']:
                plot_hic_boxplots(
                    name = subworkflow_name,
                    entry = x,
                    data_df = subset_df,
                    list_of_processes = subworkflow_processes,
                    verbose = options.verbose,
                    outdir = outdir
                )

    #print(ProjectStats(usable_data))
    """ 
        a1, a2, a3 = generate_genome_vs_runtime(subset_df)

        b1, b2, b3 = generate_clade_vs_runtime(subset_df)

        c1, c2, c3 = generate_family_vs_runtime(subset_df)

        d1, d2, d3 = generate_longread_vs_runtime(subset_df)

        e1, e2, e3 = generate_hic_vs_runtime(subset_df)

        f1, f2, f3 = generate_3d_graphs(subset_df)
    """
    cli = print_report(header_df, empty_files)

    """ html_string = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>
                body{
                    margin:0 100;
                    background:whitesmoke;
                }
                .boxy{
                    float: left;
                    width: 50%;
                    padding: 50px;
                }
                .row{
                    width: 100%;
                }
                p {text-align: center;}
            </style>
            <script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
        </head>
        <h1>TreeVal Summary Stats Report</h1>
        <div class="row">
            <div class="boxy">
                <div>
                    <div class="text-uppercase text-primary font-weight-bold text-xs mb-1"><span>Rows of Data</span></div>
                    
                    <div class="text-dark font-weight-bold h5 mb-0"><span> ''' + total_rows + '''</span></div>
                </div>
            </div>
            <div class="boxy">
                <div class="col mr-2">
                    <div class="text-uppercase text-success font-weight-bold text-xs mb-1"><span>Columns of Data</span></div>

                    <div class="text-dark font-weight-bold h5 mb-0"><span>''' + total_cols + '''</span></div>
                </div>
            </div>
        </div>
        <div>
            <h2> General Stats</h2>
            <p>
                ''' + cli + '''
            <p>
        </div>
        <div>
            <h2> Genome Size vs. Runtime </h2>
            <!-- *** Section 1 *** --->
                ''' + a1 + '''
                <!-- *** Section 2 *** --->
                ''' + a2 + '''
                <!-- *** Section 3 *** --->
                ''' + a3 + '''
        </div>
        <div>
            <h2> Clade vs. Runtime </h2>
            <!-- *** Section 1 *** --->
                ''' + b1 + '''
                <!-- *** Section 2 *** --->
                ''' + b2 + '''
                <!-- *** Section 3 *** --->
                ''' + b3 + '''
        </div>
        <div>
            <h2> Family vs. Runtime </h2>
            <!-- *** Section 1 *** --->
                ''' + c1 + '''
                <!-- *** Section 2 *** --->
                ''' + c2 + '''
                <!-- *** Section 3 *** --->
                ''' + c3 + '''
        </div>
        <div>
            <h2> Longread vs. Runtime </h2>
            <!-- *** Section 1 *** --->
                ''' + d1 + '''
                <!-- *** Section 2 *** --->
                ''' + d2 + '''
                <!-- *** Section 3 *** --->
                ''' + d3 + '''
        </div>
        <div>
            <h2> HiC vs. Runtime </h2>
            <!-- *** Section 1 *** --->
                ''' + e1 + '''
                <!-- *** Section 2 *** --->
                ''' + e2 + '''
                <!-- *** Section 3 *** --->
                ''' + e3 + '''
        </div>
        <div>
            <h2> 3D Graphs </h2>
            <!-- *** Section 1 *** --->
                ''' + f1 + '''
                <!-- *** Section 2 *** --->
                ''' + f2 + '''
                <!-- *** Section 3 *** --->
                ''' + f3 + '''
        </div>
        </body>
    </html>
    '''

    with open(options.output + 'TreeValSummary.html', 'w') as html_report:
        html_report.write(html_string) """

if __name__ == "__main__":
    main()
# %%
