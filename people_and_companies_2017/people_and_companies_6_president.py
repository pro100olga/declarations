# You first need to run files: 
# people_and_companies_1_get_data.py
# people_and_companies_2_correct_data.py 
# people_and_companies_3_graphs.py

import networkx as nx
import re
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms import bipartite

pairs['fio_post_comp'] = pairs['fio'] + ', ' + pairs['office'] + ', ' + pairs['position']

# =============================================================================
# CLOSEST NODES
# =============================================================================

def graph_community_of_node_neigh_level_n(g_source, node, level_n):
    
    g_com = nx.Graph(g_source.subgraph(node))
    
    for i in range(level_n):
        for node in list(g_com.nodes()):
            for node_neigh in list(g_source.neighbors(node)):
                if not g_com.has_edge(node, node_neigh):
                    g_com.add_edge(node, node_neigh)
    
    for node in g_com.nodes():
        if bool(re.search('nacp_', node)): # person
            g_com.node[node]['label'] = 'person'
            g_com.node[node]['name'] = pairs.loc[pairs['id'] == node]['fio_post_comp'].drop_duplicates()
            g_com.node[node]['company_ua'] = -1
        else:
            g_com.node[node]['label'] = 'company'
            g_com.node[node]['name'] = companies_names[companies_names['company_id_r'] == node]['company_name'].values[0]
            g_com.node[node]['company_ua'] = companies_names[companies_names['company_id_r'] == node]['company_ua'].values[0]
    
    return g_com

def graph_community_of_node_neigh_level_n_short(g_source, node, level_n):
    
    g_com = nx.Graph(g_source.subgraph(node))
    
    for i in range(level_n):
        for node in list(g_com.nodes()):
            for node_neigh in list(g_source.neighbors(node)):
                if not g_com.has_edge(node, node_neigh):
                    g_com.add_edge(node, node_neigh)
    
    return g_com

g_pres_com = graph_community_of_node_neigh_level_n(g, 'nacp_c9e4d7dd-d6b7-44b8-9e26-12e756d36e04', 2)

# Chart of president + companies + people

g_pres_com_node_colors = []

for node in g_pres_com.nodes(data = True):
    if node[0] == 'nacp_c9e4d7dd-d6b7-44b8-9e26-12e756d36e04':
        g_pres_com_node_colors.append('red')
    elif bool(re.search('nacp_', node[0])):
        g_pres_com_node_colors.append('lightblue')
    else:
        g_pres_com_node_colors.append('gold')

nx.draw(g_pres_com,
        node_size = 10,
        node_color = g_pres_com_node_colors,
        width = 0.05)

plt.savefig("g_pres_com_2.png", format="PNG", dpi = 200, figsize = (8,6))

del g_pres_com_node_colors

# Prepare table for this chart

g_pres_com_edges_df = pd.DataFrame(data = list(g_pres_com.edges), 
                                   columns=['node1', 'node2'])

g_pres_com_edges_df['node_person'] = np.where(g_pres_com_edges_df['node1'].str.contains('nacp'), 
                   g_pres_com_edges_df['node1'], g_pres_com_edges_df['node2'])

g_pres_com_edges_df['node_company'] = np.where(g_pres_com_edges_df['node1'].str.contains('nacp'), 
                   g_pres_com_edges_df['node2'], g_pres_com_edges_df['node1'])

g_pres_com_edges_df = g_pres_com_edges_df[['node_person', 'node_company']]

g_pres_com_edges_df = g_pres_com_edges_df.merge(pairs[['id', 'fio_post_comp']].drop_duplicates(), 
                                                left_on = 'node_person', right_on = 'id', how = 'left')

g_pres_com_edges_df = g_pres_com_edges_df.merge(companies_names[['company_id_r', 'company_name']], 
                                                left_on = 'node_company', right_on = 'company_id_r', how = 'left')

g_pres_com_edges_df = g_pres_com_edges_df[['node_person', 'node_company', 'fio_post_comp', 'company_name']]

g_pres_com_edges_df.to_csv("g_pres_com_edges_df.csv", sep = "|", encoding = "utf-8")

