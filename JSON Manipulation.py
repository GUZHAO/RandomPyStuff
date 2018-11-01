import json

with open('C:/Users/gz056/Downloads/dep.json') as dep_file:
    data = json.load(dep_file)
cu1 = ['f2438bff-8d2d-49ae-91d7-9b71737cc98d',
       'cc51d56d-2d3f-4205-b208-25a92f9e2934',
       'e599ebe3-7b15-4df9-938e-71eaa9fec451',
       '3b234caa-a034-45b7-9534-b86adfca886a',
       '81f4dc94-a38d-4e7c-8591-12db4b95094b',
       '61dfdbdb-6adf-4cbe-b511-ddfc4f90292a',
       'e02f4645-55f8-4196-86c8-ee53537479b0',
       'bcafa80b-27d2-4485-a946-cd213cf83f96',
       '63ff3e1d-4eaf-47e3-bc01-8766b6eb956e',
       '28c70db4-8a99-48c8-bf46-dbcea2cf08e5',
       '5a027324-cede-4c17-a805-539931d80cac',
       '519061be-0f8b-4232-ad95-617c68c86012',
       'd806ce74-72fc-4478-9ff1-c33ef02e1ba1']
cu2 = ['fc436d1e-ae38-4cd5-98e5-f608209bb0bf',
       '6a05ef69-d677-478c-9f70-baf03903a172']
cu3 = ['247fd73f-d12a-4baa-aad3-5349d09c78b1']
cu4 = ['b29ca2c6-0f6d-48ca-a5a7-44e926ad41e8',
       'bc7740c6-b6d4-4197-bc15-3f92f41bd8e5',
       'c1b3452b-a23a-4cad-abcd-ac38f540afb7',
       'f66c64a2-ecf5-4f3e-982c-cd6972bf1ed8',
       'ef73108a-59da-4237-b61e-bbb82024338e',
       '6202ac73-5ed9-47c9-a00f-44b7a71f88f5',
       '41083d41-9926-4353-be03-d76044fbb4c8',
       '58b4d953-dd07-4b15-8648-61c8bf355707',
       '33097433-6b14-496e-8aa6-567c7dbe3dbb',
       '6c55b4a3-5536-4c96-b5ca-ae8abc8efaf2',
       '20c06c31-0962-4d35-9862-53178904b5cc',
       'dc8f130d-87eb-40f4-8611-95c8811f3a95',
       '3ea1ae17-fae3-498a-9acb-0eea357e9092',
       'dc0f3abe-d2df-475b-ba69-608d8b640d93',
       'f6e68a5c-77bb-401d-8ace-3d3fd92f9c11',
       '1e52ee2c-cbc3-4028-b6fc-9a1e4a1eab0c',
       'ef1a8b2a-437f-4433-80c2-a8a314b0f005',
       '203d7a38-fe84-4334-a17b-dcd7e904b930',
       'b87f9294-7e3a-4b90-ac0c-66cb3204dbb8']
cu5 = ['a0e705a1-0cd2-42d1-a9ae-1e68050127ff']
cu6 = ['69d05cd3-43b3-4d19-ad50-18a45e3e7e49',
       '82607aa6-d261-42fa-a72b-09a3f00129df',
       'c5e8c316-4b47-45a2-8de6-f2564fbe27c7',
       'b22829e3-fb08-4997-a2f9-c5420dae9cf6',
       'b6e8f978-c6ae-4d8a-a16a-ea1121685960',
       'b631b487-7d9a-4faa-a555-f7c327235a93',
       '7f0b5b70-4112-40ef-9abe-2e901c732421',
       'd25b19ab-4be1-4d7f-971d-428e2f809b2a',
       '67e6308d-9a4b-49d5-a423-d445a784eb75']
cu7 = ['14d0ebf8-a690-4f80-a2d1-5b1f6583240f',
       'b222083a-05f6-444b-a845-15861188d2de',
       'e680826b-c8fc-4236-bcc1-fd955e16aba9',
       '5ecd8f30-0674-4a0e-aba1-416ecac46176']
cu8 = ['7fe6e95e-da7a-4000-a0cf-3f48d3b0a140']
cu9 = ['47c59bc7-f997-46b3-b5d8-8d1639892a1e']
cu10 = ['476d25e9-626a-440a-8097-3f8e9155f5bd']
ana1 = 'Gu/Mark'
ana2 = 'Angela/Mark'
ana3 = 'Sarah/Shobana'
ana4 = 'Paula/Bobby'
ana5 = 'Mark/Gu'
ana6 = 'Sarah/Mark'
ana7 = 'Bobby/Shobana'
ana8 = 'Paula/Gu'
ana9 = 'Shobana/Mark'
ana10 = 'Angela/Gu'

for i in range(len(data['list']['entry'])):
    data['list']['entry'][i]['unit'] = ''
    data['list']['entry'][i]['analyst'] = ''


def loop_dep_list(element, cu_name, ana_name):
    for i in range(len(data['list']['entry'])):
        if data['list']['entry'][i]['id'] in element:
            data['list']['entry'][i]['unit'] = cu_name
            data['list']['entry'][i]['analyst'] = ana_name

    # cu_list.append({'unit': cu_name, 'department': data['list']['entry'][i]['fields']['depNm'],
    #                 'department_id': data['list']['entry'][i]['id']})


loop_dep_list(cu1, 'cu1', ana1)
loop_dep_list(cu2, 'cu2', ana2)
loop_dep_list(cu3, 'cu3', ana3)
loop_dep_list(cu4, 'cu4', ana4)
loop_dep_list(cu5, 'cu5', ana5)
loop_dep_list(cu6, 'cu6', ana6)
loop_dep_list(cu7, 'cu7', ana7)
loop_dep_list(cu8, 'cu8', ana8)
loop_dep_list(cu9, 'cu9', ana9)
loop_dep_list(cu10, 'cu10', ana10)
with open('C:/Users/gz056/Downloads/data.json', 'w') as outfile:
    json.dump(data['list']['entry'], outfile)
