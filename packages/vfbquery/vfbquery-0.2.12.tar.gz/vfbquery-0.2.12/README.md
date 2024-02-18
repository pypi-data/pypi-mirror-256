# VFBquery

to setup requirements:
```bash
pip install --upgrade vfbquery
```

To get term info for a term:
get_term_info(ID)

e.g.
```python
import vfbquery as vfb
```
Class example:
```python
vfb.get_term_info('FBbt_00003748')
```
```json
{
   'Name':'medulla',
   'Id':'FBbt_00003748',
   'SuperTypes':[
      'Entity',
      'Adult',
      'Anatomy',
      'Class',
      'Nervous_system',
      'Synaptic_neuropil',
      'Synaptic_neuropil_domain',
      'Visual_system'
   ],
   'Meta':{
      'Name':'[medulla](FBbt_00003748)',
      'Description':'The second optic neuropil, sandwiched between the lamina and the lobula complex. It is divided into 10 layers: 1-6 make up the outer (distal) medulla, the seventh (or serpentine) layer exhibits a distinct architecture and layers 8-10 make up the inner (proximal) medulla (Ito et al., 2014).',
      'Comment':'',
      'Types':'[synaptic neuropil domain](FBbt_00040007)',
      'Relationships':'[develops from](RO_0002202): [medulla anlage](FBbt_00001935); [is part of](BFO_0000050): [adult optic lobe](FBbt_00003701)',
      'Cross References':'![Insect Brain DB](https://insectbraindb.org/app/assets/images/Megalopta_frontal.png) [Insect Brain DB](https://insectbraindb.org/): [38](https://insectbraindb.org/app/structures/38)'
   },
   'Tags':[
      'Adult',
      'Nervous_system',
      'Synaptic_neuropil_domain',
      'Visual_system'
   ],
   'Queries':[
      {
         'query':'ListAllAvailableImages',
         'label':'List all available images of medulla',
         'function':'get_instances',
         'takes':{
            'short_form':{
               '$and':[
                  'Class',
                  'Anatomy'
               ]
            },
            'default':{
               'short_form':'FBbt_00003748'
            }
         },
         'preview':0,
         'preview_columns':[
            'id',
            'label',
            'tags',
            'thumbnail'
         ],
         'preview_results':{
            'headers':{
               'id':{
                  'title':'Add',
                  'type':'selection_id',
                  'order':-1
               },
               'label':{
                  'title':'Name',
                  'type':'markdown',
                  'order':0,
                  'sort':{
                     0:'Asc'
                  }
               },
               'tags':{
                  'title':'Gross Types',
                  'type':'tags',
                  'order':3
               },
               'thumbnail':{
                  'title':'Thumbnail',
                  'type':'markdown',
                  'order':9
               }
            },
            'rows':[
               
            ]
         },
         'output_format':'table',
         'count':4
      }
   ],
   'IsIndividual':False,
   'IsClass':True,
   'Examples':{
      'VFB_00017894':[
         {
            'id':'VFB_00030624',
            'label':'medulla on adult brain template JFRC2',
            'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0003/0624/VFB_00017894/thumbnail.png',
            'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0003/0624/VFB_00017894/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0003/0624/VFB_00017894/volume.nrrd',
            'wlz':'https://www.virtualflybrain.org/data/VFB/i/0003/0624/VFB_00017894/volume.wlz',
            'obj':'https://www.virtualflybrain.org/data/VFB/i/0003/0624/VFB_00017894/volume_man.obj'
         }
      ],
      'VFB_00030786':[
         {
            'id':'VFB_00030810',
            'label':'medulla on adult brain template Ito2014',
            'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0003/0810/thumbnail.png',
            'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0003/0810/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0003/0810/volume.nrrd',
            'wlz':'https://www.virtualflybrain.org/data/VFB/i/0003/0810/volume.wlz',
            'obj':'https://www.virtualflybrain.org/data/VFB/i/0003/0810/volume_man.obj'
         }
      ],
      'VFB_00101384':[
         {
            'id':'VFB_00101385',
            'label':'ME(R) on JRC_FlyEM_Hemibrain',
            'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/1385/VFB_00101384/thumbnail.png',
            'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/1385/VFB_00101384/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0010/1385/VFB_00101384/volume.nrrd',
            'wlz':'https://www.virtualflybrain.org/data/VFB/i/0010/1385/VFB_00101384/volume.wlz',
            'obj':'https://www.virtualflybrain.org/data/VFB/i/0010/1385/VFB_00101384/volume_man.obj'
         }
      ],
      'VFB_00101567':[
         {
            'id':'VFB_00102107',
            'label':'ME on JRC2018Unisex adult brain',
            'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/thumbnail.png',
            'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/volume.nrrd',
            'wlz':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/volume.wlz',
            'obj':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/volume_man.obj'
         }
      ]
   },
   'IsTemplate':False
}
```
Individual example:
```python
vfb.get_term_info('VFB_00000001')
```

```json
{
   'Name':'fru-M-200266',
   'Id':'VFB_00000001',
   'SuperTypes':[
      'Entity',
      'Adult',
      'Anatomy',
      'Cell',
      'Expression_pattern_fragment',
      'Individual',
      'Nervous_system',
      'Neuron',
      'VFB',
      'has_image',
      'FlyCircuit',
      'NBLAST'
   ],
   'Meta':{
      'Name':'[fru-M-200266](VFB_00000001)',
      'Description':'',
      'Comment':'OutAge: Adult 5~15 days',
      'Types':'[adult DM6 lineage neuron](FBbt_00050144); [expression pattern fragment](VFBext_0000004)',
      'Relationships':'[expresses](RO_0002292): [Scer\\GAL4[fru.P1.D]](FBal0276838); [is part of](BFO_0000050): [Scer\\GAL4[fru.P1.D] expression pattern](VFBexp_FBal0276838), [adult brain](FBbt_00003624), [male organism](FBbt_00007004); [overlaps](RO_0002131): [adult antennal lobe](FBbt_00007401), [adult crepine](FBbt_00045037), [adult lateral accessory lobe](FBbt_00003681), [superior posterior slope](FBbt_00045040), [vest](FBbt_00040041)',
      'Cross References':'[FlyCircuit 1.0](http://flycircuit.tw): [fru-M-200266](http://flycircuit.tw/modules.php?name=clearpage&op=detail_table&neuron=fru-M-200266)'
   },
   'Tags':[
      'Adult',
      'Expression_pattern_fragment',
      'Nervous_system',
      'Neuron'
   ],
   'Queries':[
      {
         'query':'SimilarMorphologyTo',
         'label':'Find similar neurons to fru-M-200266',
         'function':'get_similar_neurons',
         'takes':{
            'short_form':{
               '$and':[
                  'Individual',
                  'Neuron'
               ]
            },
            'default':{
               'neuron':'VFB_00000001',
               'similarity_score':'NBLAST_score'
            }
         },
         'preview':5,
         'preview_columns':[
            'id',
            'score',
            'name',
            'tags',
            'thumbnail'
         ],
         'preview_results':{
            'headers':{
               'id':{
                  'title':'Add',
                  'type':'selection_id',
                  'order':-1
               },
               'score':{
                  'title':'Score',
                  'type':'numeric',
                  'order':1,
                  'sort':{
                     0:'Desc'
                  }
               },
               'name':{
                  'title':'Name',
                  'type':'markdown',
                  'order':1,
                  'sort':{
                     1:'Asc'
                  }
               },
               'tags':{
                  'title':'Tags',
                  'type':'tags',
                  'order':2
               },
               'thumbnail':{
                  'title':'Thumbnail',
                  'type':'markdown',
                  'order':9
               }
            },
            'rows':[
               {
                  'id':'VFB_00000333',
                  'score':0.61,
                  'name':'[fru-M-000204](VFB_00000333)',
                  'tags':'Nervous_system|Expression_pattern_fragment|Neuron|Adult',
                  'thumbnail':"[![fru-M-000204 aligned to JRC2018Unisex](http://virtualflybrain.org/reports/VFB_00000333/thumbnail.png 'fru-M-000204 aligned to JRC2018Unisex')](VFB_00101567,VFB_00000333)"
               },
               {
                  'id':'VFB_00000333',
                  'score':0.61,
                  'name':'[fru-M-000204](VFB_00000333)',
                  'tags':'Nervous_system|Expression_pattern_fragment|Neuron|Adult',
                  'thumbnail':"[![fru-M-000204 aligned to adult brain template JFRC2](http://virtualflybrain.org/reports/VFB_00000333/thumbnail.png 'fru-M-000204 aligned to adult brain template JFRC2')](VFB_00017894,VFB_00000333)"
               },
               {
                  'id':'VFB_00002439',
                  'score':0.6,
                  'name':'[fru-M-900020](VFB_00002439)',
                  'tags':'Expression_pattern_fragment|Nervous_system|Neuron|Adult',
                  'thumbnail':"[![fru-M-900020 aligned to adult brain template JFRC2](http://www.virtualflybrain.org/data/VFB/i/0000/2439/VFB_00017894/thumbnail.png 'fru-M-900020 aligned to adult brain template JFRC2')](VFB_00017894,VFB_00002439)"
               },
               {
                  'id':'VFB_00002439',
                  'score':0.6,
                  'name':'[fru-M-900020](VFB_00002439)',
                  'tags':'Expression_pattern_fragment|Nervous_system|Neuron|Adult',
                  'thumbnail':"[![fru-M-900020 aligned to JRC2018Unisex](http://www.virtualflybrain.org/data/VFB/i/0000/2439/VFB_00101567/thumbnail.png 'fru-M-900020 aligned to JRC2018Unisex')](VFB_00101567,VFB_00002439)"
               },
               {
                  'id':'VFB_00001880',
                  'score':0.59,
                  'name':'[fru-M-100041](VFB_00001880)',
                  'tags':'Nervous_system|Expression_pattern_fragment|Neuron|Adult',
                  'thumbnail':"[![fru-M-100041 aligned to JRC2018Unisex](http://www.virtualflybrain.org/data/VFB/i/0000/1880/VFB_00101567/thumbnail.png 'fru-M-100041 aligned to JRC2018Unisex')](VFB_00101567,VFB_00001880)"
               }
            ]
         },
         'output_format':'table',
         'count':60
      }
   ],
   'IsIndividual':True,
   'Images':{
      'VFB_00017894':[
         {
            'id':'VFB_00000001',
            'label':'fru-M-200266',
            'thumbnail':'https://virtualflybrain.org/reports/VFB_00000001/thumbnail.png',
            'thumbnail_transparent':'https://virtualflybrain.org/reports/VFB_00000001/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0000/0001/VFB_00017894/volume.nrrd',
            'wlz':'https://virtualflybrain.org/reports/VFB_00000001/volume.wlz',
            'obj':'https://virtualflybrain.org/reports/VFB_00000001/volume.obj',
            'swc':'https://www.virtualflybrain.org/data/VFB/i/0000/0001/VFB_00017894/volume.swc'
         }
      ],
      'VFB_00101567':[
         {
            'id':'VFB_00000001',
            'label':'fru-M-200266',
            'thumbnail':'https://virtualflybrain.org/reports/VFB_00000001/thumbnail.png',
            'thumbnail_transparent':'https://virtualflybrain.org/reports/VFB_00000001/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0000/0001/VFB_00101567/volume.nrrd',
            'wlz':'https://virtualflybrain.org/reports/VFB_00000001/volume.wlz',
            'obj':'https://virtualflybrain.org/reports/VFB_00000001/volume.obj',
            'swc':'https://www.virtualflybrain.org/data/VFB/i/0000/0001/VFB_00101567/volume.swc'
         }
      ]
   },
   'IsClass':False,
   'IsTemplate':False,
   'Licenses':{
      0:{
         'iri':'http://virtualflybrain.org/reports/VFBlicense_FlyCircuit_License',
         'short_form':'VFBlicense_FlyCircuit_License',
         'label':'FlyCircuit License',
         'icon':'',
         'source':'FlyCircuit 1.0 - single neurons (Chiang2010)',
         'source_iri':'http://virtualflybrain.org/reports/Chiang2010'
      }
   }
}
```
Template example:
```python
vfb.get_term_info('VFB_00101567')
```

```json
{
   'Name':'JRC2018Unisex',
   'Id':'VFB_00101567',
   'SuperTypes':[
      'Entity',
      'Adult',
      'Anatomy',
      'Individual',
      'Nervous_system',
      'Template',
      'has_image'
   ],
   'Meta':{
      'Name':'[JRC2018Unisex](VFB_00101567)',
      'Description':'Janelia 2018 unisex, averaged adult brain template',
      'Comment':'',
      'Types':'[adult brain](FBbt_00003624)'
   },
   'Tags':[
      'Adult',
      'Nervous_system'
   ],
   'Queries':[
      
   ],
   'IsIndividual':True,
   'Images':{
      'VFBc_00101567':[
         {
            'id':'VFBc_00101567',
            'label':'JRC2018Unisex_c',
            'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/thumbnail.png',
            'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/thumbnailT.png',
            'nrrd':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/volume.nrrd',
            'wlz':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/volume.wlz',
            'obj':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/volume_man.obj',
            'index':0,
            'center':{
               'X':605.0,
               'Y':283.0,
               'Z':87.0
            },
            'extent':{
               'X':1211.0,
               'Y':567.0,
               'Z':175.0
            },
            'voxel':{
               'X':0.5189161,
               'Y':0.5189161,
               'Z':1.0
            },
            'orientation':'LPS'
         }
      ]
   },
   'IsClass':False,
   'IsTemplate':True,
   'Domains':{
      0:{
         'id':'VFB_00101567',
         'label':'JRC2018Unisex',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/thumbnailT.png',
         'index':0,
         'center':None,
         'type_label':'adult brain',
         'type_id':'FBbt_00003624'
      },
      3:{
         'id':'VFB_00102107',
         'label':'ME on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/thumbnailT.png',
         'index':3,
         'center':None,
         'type_label':'medulla',
         'type_id':'FBbt_00003748'
      },
      4:{
         'id':'VFB_00102108',
         'label':'AME on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2108/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2108/VFB_00101567/thumbnailT.png',
         'index':4,
         'center':None,
         'type_label':'accessory medulla',
         'type_id':'FBbt_00045003'
      },
      5:{
         'id':'VFB_00102109',
         'label':'LO on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2109/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2109/VFB_00101567/thumbnailT.png',
         'index':5,
         'center':None,
         'type_label':'lobula',
         'type_id':'FBbt_00003852'
      },
      6:{
         'id':'VFB_00102110',
         'label':'LOP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2110/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2110/VFB_00101567/thumbnailT.png',
         'index':6,
         'center':None,
         'type_label':'lobula plate',
         'type_id':'FBbt_00003885'
      },
      7:{
         'id':'VFB_00102114',
         'label':'CA on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2114/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2114/VFB_00101567/thumbnailT.png',
         'index':7,
         'center':None,
         'type_label':'calyx of adult mushroom body',
         'type_id':'FBbt_00007385'
      },
      10:{
         'id':'VFB_00102118',
         'label':'PED on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2118/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2118/VFB_00101567/thumbnailT.png',
         'index':10,
         'center':None,
         'type_label':'pedunculus of adult mushroom body',
         'type_id':'FBbt_00007453'
      },
      11:{
         'id':'VFB_00102119',
         'label':'aL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2119/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2119/VFB_00101567/thumbnailT.png',
         'index':11,
         'center':None,
         'type_label':'adult mushroom body alpha-lobe',
         'type_id':'FBbt_00110657'
      },
      12:{
         'id':'VFB_00102121',
         'label':"a\\'L on JRC2018Unisex adult brain",
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2121/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2121/VFB_00101567/thumbnailT.png',
         'index':12,
         'center':None,
         'type_label':"adult mushroom body alpha'-lobe",
         'type_id':'FBbt_00013691'
      },
      13:{
         'id':'VFB_00102123',
         'label':'bL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2123/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2123/VFB_00101567/thumbnailT.png',
         'index':13,
         'center':None,
         'type_label':'adult mushroom body beta-lobe',
         'type_id':'FBbt_00110658'
      },
      14:{
         'id':'VFB_00102124',
         'label':"b\\'L on JRC2018Unisex adult brain",
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2124/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2124/VFB_00101567/thumbnailT.png',
         'index':14,
         'center':None,
         'type_label':"adult mushroom body beta'-lobe",
         'type_id':'FBbt_00013694'
      },
      15:{
         'id':'VFB_00102133',
         'label':'gL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2133/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2133/VFB_00101567/thumbnailT.png',
         'index':15,
         'center':None,
         'type_label':'adult mushroom body gamma-lobe',
         'type_id':'FBbt_00013695'
      },
      16:{
         'id':'VFB_00102134',
         'label':'FB on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2134/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2134/VFB_00101567/thumbnailT.png',
         'index':16,
         'center':None,
         'type_label':'fan-shaped body',
         'type_id':'FBbt_00003679'
      },
      18:{
         'id':'VFB_00102135',
         'label':'EB on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2135/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2135/VFB_00101567/thumbnailT.png',
         'index':18,
         'center':None,
         'type_label':'ellipsoid body',
         'type_id':'FBbt_00003678'
      },
      19:{
         'id':'VFB_00102137',
         'label':'PB on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2137/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2137/VFB_00101567/thumbnailT.png',
         'index':19,
         'center':None,
         'type_label':'protocerebral bridge',
         'type_id':'FBbt_00003668'
      },
      21:{
         'id':'VFB_00102139',
         'label':'BU on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2139/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2139/VFB_00101567/thumbnailT.png',
         'index':21,
         'center':None,
         'type_label':'bulb',
         'type_id':'FBbt_00003682'
      },
      22:{
         'id':'VFB_00102140',
         'label':'LAL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2140/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2140/VFB_00101567/thumbnailT.png',
         'index':22,
         'center':None,
         'type_label':'adult lateral accessory lobe',
         'type_id':'FBbt_00003681'
      },
      23:{
         'id':'VFB_00102141',
         'label':'AOTU on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2141/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2141/VFB_00101567/thumbnailT.png',
         'index':23,
         'center':None,
         'type_label':'anterior optic tubercle',
         'type_id':'FBbt_00007059'
      },
      24:{
         'id':'VFB_00102146',
         'label':'AVLP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2146/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2146/VFB_00101567/thumbnailT.png',
         'index':24,
         'center':None,
         'type_label':'anterior ventrolateral protocerebrum',
         'type_id':'FBbt_00040043'
      },
      25:{
         'id':'VFB_00102148',
         'label':'PVLP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2148/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2148/VFB_00101567/thumbnailT.png',
         'index':25,
         'center':None,
         'type_label':'posterior ventrolateral protocerebrum',
         'type_id':'FBbt_00040042'
      },
      26:{
         'id':'VFB_00102152',
         'label':'PLP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2152/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2152/VFB_00101567/thumbnailT.png',
         'index':26,
         'center':None,
         'type_label':'posterior lateral protocerebrum',
         'type_id':'FBbt_00040044'
      },
      27:{
         'id':'VFB_00102154',
         'label':'WED on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2154/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2154/VFB_00101567/thumbnailT.png',
         'index':27,
         'center':None,
         'type_label':'wedge',
         'type_id':'FBbt_00045027'
      },
      28:{
         'id':'VFB_00102159',
         'label':'LH on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2159/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2159/VFB_00101567/thumbnailT.png',
         'index':28,
         'center':None,
         'type_label':'adult lateral horn',
         'type_id':'FBbt_00007053'
      },
      29:{
         'id':'VFB_00102162',
         'label':'SLP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2162/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2162/VFB_00101567/thumbnailT.png',
         'index':29,
         'center':None,
         'type_label':'superior lateral protocerebrum',
         'type_id':'FBbt_00007054'
      },
      30:{
         'id':'VFB_00102164',
         'label':'SIP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2164/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2164/VFB_00101567/thumbnailT.png',
         'index':30,
         'center':None,
         'type_label':'superior intermediate protocerebrum',
         'type_id':'FBbt_00045032'
      },
      31:{
         'id':'VFB_00102170',
         'label':'SMP on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2170/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2170/VFB_00101567/thumbnailT.png',
         'index':31,
         'center':None,
         'type_label':'superior medial protocerebrum',
         'type_id':'FBbt_00007055'
      },
      32:{
         'id':'VFB_00102171',
         'label':'CRE on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2171/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2171/VFB_00101567/thumbnailT.png',
         'index':32,
         'center':None,
         'type_label':'adult crepine',
         'type_id':'FBbt_00045037'
      },
      33:{
         'id':'VFB_00102174',
         'label':'ROB on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2174/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2174/VFB_00101567/thumbnailT.png',
         'index':33,
         'center':None,
         'type_label':'adult round body',
         'type_id':'FBbt_00048509'
      },
      34:{
         'id':'VFB_00102175',
         'label':'RUB on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2175/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2175/VFB_00101567/thumbnailT.png',
         'index':34,
         'center':None,
         'type_label':'rubus',
         'type_id':'FBbt_00040038'
      },
      35:{
         'id':'VFB_00102176',
         'label':'SCL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2176/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2176/VFB_00101567/thumbnailT.png',
         'index':35,
         'center':None,
         'type_label':'superior clamp',
         'type_id':'FBbt_00040048'
      },
      36:{
         'id':'VFB_00102179',
         'label':'ICL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2179/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2179/VFB_00101567/thumbnailT.png',
         'index':36,
         'center':None,
         'type_label':'inferior clamp',
         'type_id':'FBbt_00040049'
      },
      37:{
         'id':'VFB_00102185',
         'label':'IB on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2185/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2185/VFB_00101567/thumbnailT.png',
         'index':37,
         'center':None,
         'type_label':'inferior bridge',
         'type_id':'FBbt_00040050'
      },
      38:{
         'id':'VFB_00102190',
         'label':'ATL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2190/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2190/VFB_00101567/thumbnailT.png',
         'index':38,
         'center':None,
         'type_label':'antler',
         'type_id':'FBbt_00045039'
      },
      39:{
         'id':'VFB_00102201',
         'label':'AL on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2201/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2201/VFB_00101567/thumbnailT.png',
         'index':39,
         'center':None,
         'type_label':'adult antennal lobe',
         'type_id':'FBbt_00007401'
      },
      40:{
         'id':'VFB_00102212',
         'label':'VES on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2212/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2212/VFB_00101567/thumbnailT.png',
         'index':40,
         'center':None,
         'type_label':'vest',
         'type_id':'FBbt_00040041'
      },
      41:{
         'id':'VFB_00102213',
         'label':'EPA on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2213/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2213/VFB_00101567/thumbnailT.png',
         'index':41,
         'center':None,
         'type_label':'epaulette',
         'type_id':'FBbt_00040040'
      },
      42:{
         'id':'VFB_00102214',
         'label':'GOR on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2214/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2214/VFB_00101567/thumbnailT.png',
         'index':42,
         'center':None,
         'type_label':'gorget',
         'type_id':'FBbt_00040039'
      },
      43:{
         'id':'VFB_00102215',
         'label':'SPS on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2215/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2215/VFB_00101567/thumbnailT.png',
         'index':43,
         'center':None,
         'type_label':'superior posterior slope',
         'type_id':'FBbt_00045040'
      },
      44:{
         'id':'VFB_00102218',
         'label':'IPS on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2218/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2218/VFB_00101567/thumbnailT.png',
         'index':44,
         'center':None,
         'type_label':'inferior posterior slope',
         'type_id':'FBbt_00045046'
      },
      45:{
         'id':'VFB_00102271',
         'label':'SAD on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2271/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2271/VFB_00101567/thumbnailT.png',
         'index':45,
         'center':None,
         'type_label':'saddle',
         'type_id':'FBbt_00045048'
      },
      46:{
         'id':'VFB_00102273',
         'label':'AMMC on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2273/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2273/VFB_00101567/thumbnailT.png',
         'index':46,
         'center':None,
         'type_label':'antennal mechanosensory and motor center',
         'type_id':'FBbt_00003982'
      },
      47:{
         'id':'VFB_00102274',
         'label':'FLA on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2274/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2274/VFB_00101567/thumbnailT.png',
         'index':47,
         'center':None,
         'type_label':'flange',
         'type_id':'FBbt_00045050'
      },
      48:{
         'id':'VFB_00102275',
         'label':'CAN on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2275/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2275/VFB_00101567/thumbnailT.png',
         'index':48,
         'center':None,
         'type_label':'cantle',
         'type_id':'FBbt_00045051'
      },
      49:{
         'id':'VFB_00102276',
         'label':'PRW on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2276/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2276/VFB_00101567/thumbnailT.png',
         'index':49,
         'center':None,
         'type_label':'prow',
         'type_id':'FBbt_00040051'
      },
      50:{
         'id':'VFB_00102280',
         'label':'GNG on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2280/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2280/VFB_00101567/thumbnailT.png',
         'index':50,
         'center':None,
         'type_label':'adult gnathal ganglion',
         'type_id':'FBbt_00014013'
      },
      59:{
         'id':'VFB_00102281',
         'label':'GA on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2281/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2281/VFB_00101567/thumbnailT.png',
         'index':59,
         'center':None,
         'type_label':'gall',
         'type_id':'FBbt_00040060'
      },
      94:{
         'id':'VFB_00102282',
         'label':'NO on JRC2018Unisex adult brain',
         'thumbnail':'https://www.virtualflybrain.org/data/VFB/i/0010/2282/VFB_00101567/thumbnail.png',
         'thumbnail_transparent':'https://www.virtualflybrain.org/data/VFB/i/0010/2282/VFB_00101567/thumbnailT.png',
         'index':94,
         'center':None,
         'type_label':'nodulus',
         'type_id':'FBbt_00003680'
      }
   },
   'Licenses':{
      0:{
         'iri':'http://virtualflybrain.org/reports/VFBlicense_CC_BY_NC_SA_4_0',
         'short_form':'VFBlicense_CC_BY_NC_SA_4_0',
         'label':'CC-BY-NC-SA_4.0',
         'icon':'http://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png',
         'source':'JRC 2018 templates & ROIs',
         'source_iri':'http://virtualflybrain.org/reports/JRC2018'
      }
   }
}
```

Queries:
```python
vfb.get_instances('FBbt_00003748', return_dataframe=False)
```
```json
{
   'headers':{
      'id':{
         'title':'Add',
         'type':'selection_id',
         'order':-1
      },
      'label':{
         'title':'Name',
         'type':'markdown',
         'order':0,
         'sort':{
            0:'Asc'
         }
      },
      'parent':{
         'title':'Parent Type',
         'type':'markdown',
         'order':1
      },
      'template':{
         'title':'Template',
         'type':'markdown',
         'order':4
      },
      'tags':{
         'title':'Gross Types',
         'type':'tags',
         'order':3
      },
      'source':{
         'title':'Data Source',
         'type':'markdown',
         'order':5
      },
      'source_id':{
         'title':'Data Source',
         'type':'markdown',
         'order':6
      },
      'dataset':{
         'title':'Dataset',
         'type':'markdown',
         'order':7
      },
      'license':{
         'title':'License',
         'type':'markdown',
         'order':8
      },
      'thumbnail':{
         'title':'Thumbnail',
         'type':'markdown',
         'order':9
      }
   },
   'rows':[
      {
         'id':'VFB_00102107',
         'label':'[ME on JRC2018Unisex adult brain](VFB_00102107)',
         'tags':'Nervous_system|Adult|Visual_system|Synaptic_neuropil_domain',
         'parent':'[medulla](FBbt_00003748)',
         'source':'',
         'source_id':'',
         'template':'[JRC2018Unisex](VFB_00101567)',
         'dataset':'[JRC 2018 templates & ROIs](JRC2018)',
         'license':'',
         'thumbnail':"[![ME on JRC2018Unisex adult brain aligned to JRC2018Unisex](http://www.virtualflybrain.org/data/VFB/i/0010/2107/VFB_00101567/thumbnail.png 'ME on JRC2018Unisex adult brain aligned to JRC2018Unisex')](VFB_00101567,VFB_00102107)"
      },
      {
         'id':'VFB_00101385',
         'label':'[ME(R) on JRC_FlyEM_Hemibrain](VFB_00101385)',
         'tags':'Nervous_system|Adult|Visual_system|Synaptic_neuropil_domain',
         'parent':'[medulla](FBbt_00003748)',
         'source':'',
         'source_id':'',
         'template':'[JRC_FlyEM_Hemibrain](VFB_00101384)',
         'dataset':'[JRC_FlyEM_Hemibrain painted domains](Xu2020roi)',
         'license':'',
         'thumbnail':"[![ME(R) on JRC_FlyEM_Hemibrain aligned to JRC_FlyEM_Hemibrain](http://www.virtualflybrain.org/data/VFB/i/0010/1385/VFB_00101384/thumbnail.png 'ME(R) on JRC_FlyEM_Hemibrain aligned to JRC_FlyEM_Hemibrain')](VFB_00101384,VFB_00101385)"
      },
      {
         'id':'VFB_00030810',
         'label':'[medulla on adult brain template Ito2014](VFB_00030810)',
         'tags':'Nervous_system|Visual_system|Adult|Synaptic_neuropil_domain',
         'parent':'[medulla](FBbt_00003748)',
         'source':'',
         'source_id':'',
         'template':'[adult brain template Ito2014](VFB_00030786)',
         'dataset':'[BrainName neuropils and tracts - Ito half-brain](BrainName_Ito_half_brain)',
         'license':'',
         'thumbnail':"[![medulla on adult brain template Ito2014 aligned to adult brain template Ito2014](http://www.virtualflybrain.org/data/VFB/i/0003/0810/thumbnail.png 'medulla on adult brain template Ito2014 aligned to adult brain template Ito2014')](VFB_00030786,VFB_00030810)"
      },
      {
         'id':'VFB_00030624',
         'label':'[medulla on adult brain template JFRC2](VFB_00030624)',
         'tags':'Nervous_system|Visual_system|Adult|Synaptic_neuropil_domain',
         'parent':'[medulla](FBbt_00003748)',
         'source':'',
         'source_id':'',
         'template':'[adult brain template JFRC2](VFB_00017894)',
         'dataset':'[BrainName neuropils on adult brain JFRC2 (Jenett, Shinomya)](JenettShinomya_BrainName)',
         'license':'',
         'thumbnail':"[![medulla on adult brain template JFRC2 aligned to adult brain template JFRC2](http://www.virtualflybrain.org/data/VFB/i/0003/0624/VFB_00017894/thumbnail.png 'medulla on adult brain template JFRC2 aligned to adult brain template JFRC2')](VFB_00017894,VFB_00030624)"
      }
   ],
   'count':4
}
```

```python
vfb.get_templates(return_dataframe=False)
```
```json
{
   'headers':{
      'id':{
         'title':'Add',
         'type':'selection_id',
         'order':-1
      },
      'order':{
         'title':'Order',
         'type':'numeric',
         'order':1,
         'sort':{
            0:'Asc'
         }
      },
      'name':{
         'title':'Name',
         'type':'markdown',
         'order':1,
         'sort':{
            1:'Asc'
         }
      },
      'tags':{
         'title':'Tags',
         'type':'tags',
         'order':2
      },
      'thumbnail':{
         'title':'Thumbnail',
         'type':'markdown',
         'order':9
      },
      'dataset':{
         'title':'Dataset',
         'type':'metadata',
         'order':3
      },
      'license':{
         'title':'License',
         'type':'metadata',
         'order':4
      }
   },
   'rows':[
      {
         'id':'VFB_00101567',
         'order':1,
         'name':'[JRC2018Unisex](VFB_00101567)',
         'tags':'Nervous_system|Adult',
         'thumbnail':"[![JRC2018Unisex](http://www.virtualflybrain.org/data/VFB/i/0010/1567/VFB_00101567/thumbnail.png 'JRC2018Unisex')](VFB_00101567)",
         'dataset':'[JRC 2018 templates & ROIs](JRC2018)',
         'license':'[CC-BY-NC-SA_4.0](VFBlicense_CC_BY_NC_SA_4_0)'
      },
      {
         'id':'VFB_00200000',
         'order':2,
         'name':'[JRC2018UnisexVNC](VFB_00200000)',
         'tags':'Nervous_system|Adult|Ganglion',
         'thumbnail':"[![JRC2018UnisexVNC](http://www.virtualflybrain.org/data/VFB/i/0020/0000/VFB_00200000/thumbnail.png 'JRC2018UnisexVNC')](VFB_00200000)",
         'dataset':'[JRC 2018 templates & ROIs](JRC2018)',
         'license':'[CC-BY-NC-SA_4.0](VFBlicense_CC_BY_NC_SA_4_0)'
      },
      {
         'id':'VFB_00017894',
         'order':3,
         'name':'[adult brain template JFRC2](VFB_00017894)',
         'tags':'Nervous_system|Adult',
         'thumbnail':"[![adult brain template JFRC2](http://www.virtualflybrain.org/data/VFB/i/0001/7894/VFB_00017894/thumbnail.png 'adult brain template JFRC2')](VFB_00017894)",
         'dataset':'[FlyLight - GMR GAL4 collection (Jenett2012)](Jenett2012)',
         'license':'[CC-BY-NC-SA_4.0](VFBlicense_CC_BY_NC_SA_4_0)'
      },
      {
         'id':'VFB_00101384',
         'order':4,
         'name':'[JRC_FlyEM_Hemibrain](VFB_00101384)',
         'tags':'Nervous_system|Adult',
         'thumbnail':"[![JRC_FlyEM_Hemibrain](http://www.virtualflybrain.org/data/VFB/i/0010/1384/thumbnail.png 'JRC_FlyEM_Hemibrain')](VFB_00101384)",
         'dataset':'[JRC_FlyEM_Hemibrain painted domains](Xu2020roi)',
         'license':'[CC-BY_4.0](VFBlicense_CC_BY_4_0)'
      },
      {
         'id':'VFB_00050000',
         'order':5,
         'name':'[L1 larval CNS ssTEM - Cardona/Janelia](VFB_00050000)',
         'tags':'Nervous_system|Larva',
         'thumbnail':"[![L1 larval CNS ssTEM - Cardona/Janelia](http://www.virtualflybrain.org/data/VFB/i/0005/0000/VFB_00050000/thumbnail.png 'L1 larval CNS ssTEM - Cardona/Janelia')](VFB_00050000)",
         'dataset':'[larval hugin neurons - EM (Schlegel2016)](Schlegel2016)',
         'license':'[CC-BY_4.0](VFBlicense_CC_BY_4_0)'
      },
      {
         'id':'VFB_00050000',
         'order':5,
         'name':'[L1 larval CNS ssTEM - Cardona/Janelia](VFB_00050000)',
         'tags':'Nervous_system|Larva',
         'thumbnail':"[![L1 larval CNS ssTEM - Cardona/Janelia](http://www.virtualflybrain.org/data/VFB/i/0005/0000/VFB_00050000/thumbnail.png 'L1 larval CNS ssTEM - Cardona/Janelia')](VFB_00050000)",
         'dataset':'[Neurons involved in larval fast escape response - EM (Ohyama2016)](Ohyama2015)',
         'license':'[CC-BY-SA_4.0](VFBlicense_CC_BY_SA_4_0)'
      },
      {
         'id':'VFB_00049000',
         'order':6,
         'name':'[L3 CNS template - Wood2018](VFB_00049000)',
         'tags':'Nervous_system|Larva',
         'thumbnail':"[![L3 CNS template - Wood2018](http://www.virtualflybrain.org/data/VFB/i/0004/9000/thumbnail.png 'L3 CNS template - Wood2018')](VFB_00049000)",
         'dataset':'[L3 Larval CNS Template (Truman2016)](Truman2016)',
         'license':'[CC-BY-SA_4.0](VFBlicense_CC_BY_SA_4_0)'
      },
      {
         'id':'VFB_00100000',
         'order':7,
         'name':'[adult VNS template - Court2018](VFB_00100000)',
         'tags':'Nervous_system|Adult|Ganglion',
         'thumbnail':"[![adult VNS template - Court2018](http://www.virtualflybrain.org/data/VFB/i/0010/0000/thumbnail.png 'adult VNS template - Court2018')](VFB_00100000)",
         'dataset':'[Adult VNS neuropils (Court2017)](Court2017)',
         'license':'[CC-BY-SA_4.0](VFBlicense_CC_BY_SA_4_0)'
      },
      {
         'id':'VFB_00030786',
         'order':8,
         'name':'[adult brain template Ito2014](VFB_00030786)',
         'tags':'Nervous_system|Adult',
         'thumbnail':"[![adult brain template Ito2014](http://www.virtualflybrain.org/data/VFB/i/0003/0786/thumbnail.png 'adult brain template Ito2014')](VFB_00030786)",
         'dataset':'[BrainName neuropils and tracts - Ito half-brain](BrainName_Ito_half_brain)',
         'license':'[CC-BY-SA_4.0](VFBlicense_CC_BY_SA_4_0)'
      },
      {
         'id':'VFB_00110000',
         'order':9,
         'name':'[Adult Head (McKellar2020)](VFB_00110000)',
         'tags':'Adult|Anatomy',
         'thumbnail':"[![Adult Head (McKellar2020)](http://www.virtualflybrain.org/data/VFB/i/0011/0000/VFB_00110000/thumbnail.png 'Adult Head (McKellar2020)')](VFB_00110000)",
         'dataset':'[GAL4 lines from McKellar et al., 2020](McKellar2020)',
         'license':'[CC-BY-SA_4.0](VFBlicense_CC_BY_SA_4_0)'
      },
      {
         'id':'VFB_00120000',
         'order':10,
         'name':'[Adult T1 Leg (Kuan2020)](VFB_00120000)',
         'tags':'Adult|Anatomy',
         'thumbnail':"[![Adult T1 Leg (Kuan2020)](http://www.virtualflybrain.org/data/VFB/i/0012/0000/VFB_00120000/thumbnail.png 'Adult T1 Leg (Kuan2020)')](VFB_00120000)",
         'dataset':'[Millimeter-scale imaging of a Drosophila leg at single-neuron resolution](Kuan2020)',
         'license':'[CC-BY_4.0](VFBlicense_CC_BY_4_0)'
      }
   ],
   'count':10
}
```
