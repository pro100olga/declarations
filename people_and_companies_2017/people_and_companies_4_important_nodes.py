# You first need to run files: 
# people_and_companies_1_get_data.py
# people_and_companies_2_correct_data.py 
# people_and_companies_3_graphs.py

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import re

# Extract centrality for each node and filter top 10

g_degree_centrality = nx.degree_centrality(g)

important_nodes_threshold = sorted(g_degree_centrality.values())[-12]

important_nodes = {k: g_degree_centrality[k] for k in list(g_degree_centrality.keys()) if g_degree_centrality[k] >= important_nodes_threshold}

important_nodes = [{k: important_nodes[k] for k in important_nodes.keys() if not bool(re.search('nacp', k))}]

important_nodes

important_nodes_df = pd.DataFrame.from_dict(important_nodes[0], orient = 'index').reset_index()
important_nodes_df.columns = ['company_id_r', 'centrality']

# Add number of neighbors

important_nodes_df['n_neighbors'] = 0

for i in range(important_nodes_df.shape[0]):
    important_nodes_df.loc[i,'n_neighbors'] = g.degree()[important_nodes_df.loc[i]['company_id_r']] #len(g.neighbors(important_nodes_df.loc[i,'company_id_r']))

del i

# Add company name and save to csv

pd.DataFrame(important_nodes_df.merge(companies_names[['company_id_r', 'company_name']], on = 'company_id_r')).to_csv("important_nodes.csv", sep = "|", encoding = "utf-8")

del important_nodes_threshold, important_nodes

important_nodes_df['company_id_r']


# Create a graph with top 10 nodes 

g_important = nx.Graph()

for node in important_nodes_df['company_id_r']:
    for n_node in list(g.neighbors(node)):
        if not g_important.has_edge(node, n_node):
            g_important.add_edge(node, n_node)

del node, n_node

nodes_person = p.loc[p['id'].isin(list(g_important.nodes()))][['id','fio_post_comp']].drop_duplicates(subset = ['id','fio_post_comp'])
nodes_person['company_ua'] = -999 
nodes_person['label'] = 'person' 
nodes_person.columns = ['id', 'name', 'company_ua', 'label']

nodes_comp = companies_names[companies_names['company_id_r'].isin(list(g_important.nodes()))][['company_id_r', 'company_name', 'company_ua']].drop_duplicates(subset = ['company_id_r', 'company_name', 'company_ua'])
nodes_comp['label'] = 'company'
nodes_comp.columns = ['id', 'name', 'company_ua', 'label']

nodes = pd.concat([nodes_person, nodes_comp])

del nodes_person, nodes_comp

nx.set_node_attributes(g_important, dict(zip(list(nodes['id']), list(nodes['name']))), 'name')
nx.set_node_attributes(g_important, dict(zip(list(nodes['id']), list(nodes['company_ua']))), 'company_ua')
nx.set_node_attributes(g_important, dict(zip(list(nodes['id']), list(nodes['label']))), 'label')

del nodes

# For the chart create lists with color (company / person) and labels, as well as position

g_important_node_color = list(map(lambda x: 'lightblue' if x == 'person' else 'gold', 
                          [n[1]['label'] for n in g_important.nodes(data = True)]))

g_important_labels = dict(zip([n[0] for n in g_important.nodes(data = True)],
                              list(map(lambda x: x[1]['name'] if x[0] in list(important_nodes_df['company_id_r']) else '', 
                                       [n for n in g_important.nodes(data = True)]))))

g_important_pos = nx.spring_layout(g_important)

nx.draw(g_important, 
        pos = g_important_pos,
        node_size = 3, width = 0.1,
        node_color = g_important_node_color,
        with_labels = False)
        
nx.draw_networkx_labels(g_important, pos = g_important_pos, 
                        labels = g_important_labels, 
                        font_size = 4, font_color = 'red')

plt.savefig("g_important.png", format="PNG", dpi = 200, figsize = (4,3))

del g_important_pos, g_important_node_color, g_important_labels

# Table with company and all people for intercative chart

important_nodes_df_interactive = pd.DataFrame({'company_id_r': [], 'person_id': []})

important_nodes_df_interactive_list = important_nodes_df.loc[~important_nodes_df['company_id_r'].str.contains('nacp')][['company_id_r']]
important_nodes_df_interactive_list = list(important_nodes_df_interactive_list['company_id_r'])

for node in important_nodes_df_interactive_list:
    for n_node in list(g.neighbors(node)):
        important_nodes_df_interactive = important_nodes_df_interactive.append(pd.DataFrame({'company_id_r': [node], 'person_id': [n_node]}))

del node, n_node
       
important_nodes_df_interactive = important_nodes_df_interactive.merge(companies_names[['company_id_r', 'company_name']],
                                                                      on = 'company_id_r', how = 'left')

important_nodes_df_interactive = important_nodes_df_interactive.merge(p[['id', 'fio_post_comp']],
                                                                      left_on = 'person_id', right_on = 'id', how = 'left')

important_nodes_df_interactive = important_nodes_df_interactive.drop_duplicates()

# important_nodes_df_interactive.to_csv("important_nodes_df_interactive.csv", sep = "|", encoding = "utf-8")

important_nodes_df_interactive.to_csv("important_nodes_df_interactive.csv", sep = "|", encoding = "utf-8")

del important_nodes_df_interactive_list

# People with many companies

pairs[['id', 'company_id_r']].drop_duplicates().groupby('id').count().sort_values(by = 'company_id_r', ascending = False)
