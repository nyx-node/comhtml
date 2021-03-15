
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from lxml import html
from django.utils.html import escape,mark_safe
from json import dumps
from difflib import SequenceMatcher

#import xlsxwriter
#from IPython.display import display


def error_view(request):
    return render(request, 'error.html')
def contact_view(request):
    return render(request, 'contact.html')
def privacy_view(request):
    return render(request, 'privacy-policy.html')
def terms_view(request):
    return render(request, 'terms-of-use.html')
def compare_view(request): # *args, **kwargs
    #print(td)
    test={'error':None}
    #return HttpResponse("<h1>Hello World</h1>") # string of HTML code
    return render(request, "compare.html", test)

def results_view(request):
#def results_view(the_url):
    the_url=request.GET
    dc={}
    dclinks={}
    balises=["title","Description","SSL","Rich-Snippets",
            "h1","h2","h3","h4","h5","h6",
            "Word count",'Internal links','Images', 'Url friendly'
            ]
    for key,url in the_url.items():
        urlx={}
        try:
            req = requests.get(url)

        except:
            #return render(request, "compare.html", {'error':url})
            return redirect(error_view)
            #dc[key]={'title':{1:{'whtml':'Url not valid','nohtml':'Url not valid'}}}
            #continue
        soup = BeautifulSoup(req.text, "html.parser")
        for bal in balises:
            i=1
            res=''
            balx={}
            dc_links={}
            if bal=='SSL':
                if(str(url[:5])=='https'):
                    urlx[bal]={i:{'whtml':mark_safe("<span class='sign tick'>&#10004;</span>") ,"nohtml":mark_safe("<span class='sign tick'>&#10004;</span>")}}
                else:
                    urlx[bal]={i:{'whtml':mark_safe("<span class='sign cross'>&#10799;</span>") ,"nohtml":mark_safe("<span class='sign cross'>&#10799;</span>")}}
            elif bal=='Rich-Snippets':
                for tag in soup.find_all('script'):
                    if(str(tag.get_text).find('@context')!=-1):
                        res=res+str(tag)
                if(res!=''):
                    urlx[bal]={i:{'whtml':escape(res) ,"nohtml":mark_safe("<span class='sign tick'>&#10004;</span>")}}
                else:
                    urlx[bal]={i:{'whtml':escape(res) ,"nohtml":mark_safe("<span class='sign cross'>&#10799;</span>")}}

            elif bal=='Url friendly':
                last=url[:-1].rfind('/')
                lurl=url[last+1:]

                try:
                    titlesim=str(round(similar(urlx['title'][1]['nohtml'],lurl)*100,1))
                except:
                    titlesim="???"
                try:
                    h1sim=str(round(similar(urlx['h1'][1]['nohtml'],lurl)*100,1))
                except:
                    titlesim="???"
                urlx[bal]={i:{'whtml':'title and url: '+ titlesim +'%   H1 and url: '+h1sim+'%' ,
                "nohtml":'title and url: '+ titlesim +'%          H1 and url: '+h1sim+'%' }}


            elif bal=='Images':
                for tag in soup.find_all('img'):
                    try:
                        if tag.parent.name=="a":
                            continue
                        else:
                            balx[i]={'whtml':escape(tag),'nohtml':"<alt empty>" if tag['alt']=='' else tag['alt']}
                    except:
                        continue
                    try:
                        balx[i]['width']=tag['width']
                    except:
                        pass
                    try:
                        balx[i]['height']=tag['height']
                    except:
                        pass
                    i=i+1
                urlx[bal]=balx
                #print(urlx[bal])

            elif bal=='Internal links':
                for link in soup.find_all('a'):
                    balx[i]={'whtml':escape(link),'nohtml':'<a>no text</a>' if (link.get_text()=='' or link.get_text()=='\n')  else link.get_text()}
                    try:
                        dc_links[i]={'href':link['href'],'whtml':escape(link)}
                    except:
                        dc_links[i]={'href':"not found",'whtml':escape(link)}
                    i=i+1
                urlx[bal]=balx
                df=pd.DataFrame.from_dict(balx, orient ='index')
                df_ref,dc_ref=link_type(url, dc_links)

                totlen=len(df['whtml'])
                nofol=len(df[df['whtml'].str.contains('nofollow')])
                urlx['Follow Info']={1:{'nohtml':'Total : '+ str(totlen) + '    nofollow : ' + str(nofol)+'    follow : '+ str(totlen-nofol)}}

                df_nofol=df[df['whtml'].str.contains('nofollow')]
                if len(df_nofol)!=0:
                    dc_nofol=df_nofol.pivot_table(index=['nohtml'],  aggfunc=len).rename(columns={"whtml":"rep"}).sort_values(by="rep",ascending=False).reset_index().to_dict('index')
                    urlx['nofollow']=dc_nofol
                else:
                    urlx['nofollow']=''

                df_fol=df[~df['whtml'].str.contains('nofollow')]
                if len(df_fol)!=0:
                    dc_fol=df_fol.pivot_table(index=['nohtml'],  aggfunc=len).rename(columns={"whtml":"rep"}).sort_values(by="rep",ascending=False).reset_index().to_dict('index')
                    urlx['follow']=dc_fol
                else:
                    urlx['follow']=''

                urlx['Link Type']={1:{"nohtml":"Identical: "+str(dc_ref["identical"])+" Internal: "+str(dc_ref["internal"])+" Extrenal: "+str(dc_ref["external"])}}

                df_ident=df_ref[df_ref.link_type=="identical"]
                if len(df_ident)!=0:
                    urlx['Identical']=df_ident[['href','whtml']].rename(columns={"href":"nohtml"}).to_dict('index')
                else:
                    urlx['Identical']=''
                df_inter=df_ref[df_ref.link_type=="internal"]
                if len(df_inter)!=0:
                    urlx['Internal']=df_inter[['href','whtml']].rename(columns={"href":"nohtml"}).to_dict('index')
                else:
                    urlx['Internal']=''
                df_exter=df_ref[df_ref.link_type=="external"]
                if len(df_exter)!=0:
                    urlx['External']=df_exter[['href','whtml']].rename(columns={"href":"nohtml"}).to_dict('index')
                else:
                    urlx['External']=''
            elif bal=='Word count':
                txt=soup.get_text()
                words=txt.split()
                nb=len(words)
                urlx[bal]={i:{'whtml':nb ,"nohtml":nb}}

            elif bal=='Description':
                desc=''
                if(soup.find('meta', {'name':'description'} )!=None):
                    desc=soup.find('meta', {'name':'description'} )
                elif(soup.find('meta', {'name':'Description'} )!=None):
                    desc=soup.find('meta', {'name':'Description'} )
                elif(soup.find('meta', {"property":"og:description"} )!=None):
                    desc=soup.find('meta', {"property":"og:description"})
                if desc=='':
                    urlx[bal]={i:{'whtml':'Warning No description found, searched in meta tags with: name description or Description and property og:description' ,
                    "nohtml":'Warning No description found, searched in meta tags with: name description or Description and property og:description' }}
                else:
                    urlx[bal]={i:{'whtml':escape(str(desc)[:str(desc).find('>')+1]) ,"nohtml":desc['content']}}
            else:
                for tag in soup.find_all(bal):

                    balx[i]={'whtml':escape(tag),'nohtml':tag.get_text()}
                    i=i+1
                urlx[bal]=balx
        dc[key]=urlx
    idc=reverse(dc)
    my_context={'idc':idc,
                'jsonidc':dumps(idc),

                'url':the_url,
                'links':dclinks}
    #print("lenght title")
    #print(idc)
    #print("end")
    return render(request, "results.html", my_context)

def reverse(dc):
    tags=[]
    for url,values in dc.items():
        for tag in values:
            if tag not in tags:
                tags.append(tag)

    idc={}
    for bal in tags :
        seq={}
        for key,values in dc.items():
            seq[key]=values[bal]
        idc[bal]=seq
        idc[bal]['max_length']=max_dc_length(seq)


    return idc
#{% if len(values1.url1)==1 and len(values1['url2'])==1 %}
def max_dc_length(seq):
    lengths=[len(values) for key,values in seq.items()]

    return max(lengths)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def link_type(url,dc_links):
    url_begin=url[:url.find("/",8)]
    df_ref=pd.DataFrame.from_dict(dc_links, orient ='index')
    df_ref.loc[df_ref['href'].str[0]=='/','link_type']='internal'
    df_ref.loc[df_ref['href'].str[0]=='#','link_type']='identical'

    df_ref.loc[df_ref['href'].str[:4]=='http','link_type']='external'

    df_ref['/pos']=df_ref['href'].str.find("/",8)
    df_ref.loc[df_ref.link_type=='external','link_type'] = df_ref[df_ref.link_type=='external'].apply(lambda x: 'internal' if x['href'][:x['/pos']] == url_begin else 'external', axis=1)
    df_ref.loc[df_ref['href']==url,'link_type']='identical'
    #return {'identical':df_ref[df_ref.link_type]=='identical'}
    #df_ref.to_excel('output1.xlsx', engine='xlsxwriter')
    return df_ref,{'identical':len(df_ref[df_ref.link_type=='identical']),
            'internal':len(df_ref[df_ref.link_type=='internal']),
            'external':len(df_ref[df_ref.link_type=='external'])}
