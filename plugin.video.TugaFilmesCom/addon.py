#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 OMaluco
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#-----------------------------------------------------------------------------------------------------------------------------------------------#
# Créditos: Este addon foi desenvolvido a partir do addon PT Video Mashup desenvolvido por enen92
#-----------------------------------------------------------------------------------------------------------------------------------------------#


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket,urlresolver


addon_id = 'plugin.video.TugaFilmesCom'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'


mensagemok = xbmcgui.Dialog().ok


#-----------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------    MENUS    -----------------------------------------------------------------#



def TFC_MenuPrincipal(artfolder):
        addDir1('[B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('[COLOR yellow]Menu Filmes[/COLOR]','url',77,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]Animação[/COLOR]','http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o?max-results=20',72,artfolder + 'banner1.png','nao','')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',74,artfolder + 'banner1.png','nao','')
	addDir('[COLOR brown]ChangeLog[/COLOR]','http://o-repositorio-maluco.googlecode.com/svn/trunk/changelogs/changelog_TugaFilmesCom.txt',89,artfolder + 'banner1.png','nao','')

def TFC_Menu_Filmes(artfolder):
        addDir1('[B][COLOR blue]Menu Filmes[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('[COLOR yellow]Ver Todos[/COLOR]','http://www.tuga-filmes.com/',72,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]Destaques[/COLOR]','http://www.tuga-filmes.com/search/label/destaque',72,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]2013[/COLOR]','http://www.tuga-filmes.com/search/label/-%20Filmes%202013',72,artfolder + 'banner1.png','nao','')
        addDir('[COLOR yellow]Top 10[/COLOR]','url',79,artfolder + 'banner1.png','nao','')
        #addDir('[COLOR yellow]Brevemente[/COLOR]','url',81,artfolder + 'banner1.png','nao','')
	addDir('[COLOR yellow]Categorias[/COLOR]','url',78,artfolder + 'banner1.png','nao','')
	if selfAddon.getSetting('hide-porno') == "false":
                addDir('[B][COLOR red]M+18[/B][/COLOR]','url',86,artfolder + 'banner1.png','nao','')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',74,artfolder + 'banner1.png','nao','')

def TFC_Menu_Series(artfolder):
        addDir1('[B][COLOR blue]Menu Séries[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('[COLOR yellow]Ver Todas[/COLOR]','url',81,artfolder + 'banner1.png','nao','')
        addDir('[COLOR yellow]Episódios Recentes[/COLOR]','http://www.tuga-filmes.tv/search/label/S%C3%A9ries',84,artfolder + 'banner1.png','nao','')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	addDir('Pesquisar','http://www.tuga-filmes.com/search?q=',85,artfolder + 'banner1.png','nao','')

def TFC_Menu_Filmes_Top_10(artfolder):
        url_top_10 = 'http://www.tuga-filmes.com/'
        top_10_source = TFC_abrir_url(url_top_10)
        addDir1('[B][COLOR blue]TOP 10[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
        filmes_top_10 = re.compile("<img alt=\'\' border=\'0\' height=\'72\' src=\'(.+?)\' width=\'72\'/>\n</a>\n</div>\n<div class=\'item-title\'><a href=\'(.+?)\'>(.+?)</a></div>\n</div>\n<div style=\'clear: both;\'>").findall(top_10_source)
	for iconimage_filmes_top_10,endereco_top_10,nome_top_10 in filmes_top_10:
		addDir(nome_top_10,endereco_top_10,73,iconimage_filmes_top_10.replace('s72-c','s320').replace('.gif','.jpg'),'nao','')

def TFC_Menu_Filmes_Por_Categorias(artfolder):
        url_categorias = 'http://www.tuga-filmes.com/'
        html_categorias_source = TFC_abrir_url(url_categorias)
        addDir1('[B][COLOR blue]Categorias[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
	html_items_categorias = re.findall("<div id=\'nav-cat\'>(.*?)</div>", html_categorias_source, re.DOTALL)
        print len(html_items_categorias)
        for item_categorias in html_items_categorias:
                filmes_por_categoria = re.compile("<a href=\'/(.+?)\'>(.+?)</a>").findall(item_categorias)
                for endereco_categoria,nome_categoria in filmes_por_categoria:
                        categoria_endereco = url_categorias + endereco_categoria
                        addDir('[COLOR yellow]' + nome_categoria + '[/COLOR]',categoria_endereco,72,artfolder + 'banner1.png','nao','')

def TFC_Menu_Filmes_Brevemente(artfolder):
        url_brevemente = 'http://www.tuga-filmes.com/'
	html_brevemente_source = TFC_abrir_url(url_brevemente)
	addDir1('[B][COLOR blue]Brevemente[/COLOR][/B]','','',artfolder + 'banner1.png',False,'')
        addDir1('','','',artfolder + 'banner1.png',False,'')
        todos_brevemente = re.findall("<marquee(.*?)</marquee>", html_brevemente_source, re.DOTALL)
        print len(todos_brevemente)
        for items_brevemente in todos_brevemente:
                item_brevemente = re.compile("<a href=\'(.+?)\' target=\'_blank\'><img height=\'140px\' src=\'(.+?)\' width=\'100px\'/></a>").findall(items_brevemente)
                for brevemente_url,iconimage_brevemente in item_brevemente:
                        nome_brevemente = re.compile('http://www.tuga-filmes.com/.+?/.+?/(.+?).html').findall(brevemente_url)
                        nome_brevemente = nome_brevemente[0].replace('-',' ')
                        addDir('[COLOR yellow]' + nome_brevemente + '[/COLOR]',brevemente_url,73,iconimage_brevemente,'nao','')
   
def TFC_Link_M18(artfolder):
        url_m18 = 'http://www.blogger.com/blogin.g?blogspotURL=http://www.tuga-filmes.info/'
	html_m18 = TFC_abrir_url(url_m18)
	m18 = re.compile('<a class="maia-button maia-button-primary" href="(.+?)" target="_parent">COMPREENDO E (.+?)</a>').findall(html_m18)
	print m18
	addDir(m18[0][1],m18[0][0],84,'','nao','')

def TFC_Menu_M18(url,artfolder):
        addDir('[COLOR yellow]Ver Todos[/COLOR]',url,84,artfolder + 'banner1.png','nao','')

        

#----------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------  Pesquisar  ---------------------------------------------------------------#



def TFC_pesquisar_filmes():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		url_pesquisa = 'http://www.tuga-filmes.com/search?q=' + str(encode)
		TFC_encontrar_fontes_filmes(url_pesquisa)

def TFC_pesquisar_series():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
	keyb.doModal()
	if (keyb.isConfirmed()):
		search = keyb.getText()
		encode=urllib.quote(search)
		url_pesquisa = 'http://www.tuga-filmes.com/search?q=' + str(encode)
		TFC_encontrar_fontes_series(url_pesquisa)	



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------  Filmes  -----------------------------------------------------------------#

		

def TFC_encontrar_fontes_filmes(url):
        pt_en = 0
	try:
		html_source = TFC_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)type=\'text/javascript\'>", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
                        versao = ''
                        pt_en_f = re.compile('<iframe (.+?)</iframe>').findall(item)
                        if '---------------------------------------' in item and len(pt_en_f) > 1: versao = '[COLOR blue] 2 VERSÕES[/COLOR]'
			urletitulo = re.compile("<a href=\'(.+?)\' title=\'(.+?)\'>").findall(item)
			qualidade_ano = re.compile('<b>VERS\xc3\x83O:.+?</b><span style="font-size: x-small;">(.+?)<').findall(item)
			thumbnail = re.compile('<img alt="" border="0" src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			ano = 'Ano'
			qualidade = ''
			e_qua = 'nao'
			calid = ''
			if qualidade_ano != []:
                                for q_a in qualidade_ano:
                                        #addDir1(q_a,'','','',False,'')
                                        a_q = re.compile('\d+')
                                        qq_aa = a_q.findall(q_a)
                                        for q_a_q_a in qq_aa:
                                                if len(q_a_q_a) == 4:
                                                        ano = q_a_q_a
                                quali = re.compile('\w+')
                                qualid = quali.findall(q_a)
                                for qua_qua in qualid:
                                        if len(qua_qua) == 4 and qua_qua == ano:
                                                e_qua = 'sim'
                                                qua_qua = ''
                                                espaco = ''
                                                espa = 0
                                        if e_qua == 'sim' and espa < 2:
                                                espa = espa + 1
                                        if e_qua == 'sim' and espa == 2:
                                                qualidade = qualidade + espaco + qua_qua
                                                espaco = ' '
                                if len(ano) < 4:
                                        ano = 'Ano'
                                        #qualidade = q_a
                                if qualidade == 'PT PT':
                                        qualidade = 'PT-PT'
                                if qualidade == '':
                                        quali_titi = urletitulo[0][1].replace('á','a')
                                        quali_titi = urletitulo[0][1].replace('é','e')
                                        quali_titi = urletitulo[0][1].replace('í','i')
                                        quali_titi = urletitulo[0][1].replace('ó','o')
                                        quali_titi = urletitulo[0][1].replace('ú','u')
                                        #addDir1(quali_titi,'','','',False,'')
                                        quali = re.compile('\w+')
                                        qualid = quali.findall(q_a)
                                        for qua_qua in qualid:
                                                qua_qua = str.capitalize(qua_qua)
                                                calid = calid + ' ' + qua_qua
                                        tita = re.compile('\w+')
                                        titalo = tita.findall(quali_titi)
                                        for tt in titalo:
                                                tt = str.capitalize(tt)
                                                if tt in calid:
                                                        qualidade = re.sub(tt,'',calid)
                                                        calid = re.sub(tt,'',calid)
                                        qqqq = re.compile('\w+')
                                        qqqqq = qqqq.findall(qualidade)
                                        for qqq in qqqqq:
                                                if qqq in quali_titi:
                                                        qualidade = qualidade.replace(qqq,'')
                                        nnnn = re.compile('\d+')
                                        nnnnn = nnnn.findall(qualidade)
                                        for nnn in nnnnn:
                                                if nnn in ano:
                                                        qualidade = qualidade.replace(nnn,'')
                                        quatit = re.compile('\s+')
                                        qualititulo = quatit.findall(qualidade)
                                        for q_t in qualititulo:
                                                if len(q_t)>1:
                                                        qualidade = qualidade.replace(q_t,'')
                                        if qualidade == 'Pt Pt':
                                                qualidade = 'PT-PT'
                        else:
                                qualidade = ''
                        if 'Pt Pt' in qualidade:
                                qualidade = qualidade.replace('Pt Pt','PT-PT')
                        if 'PT PT' in qualidade:
                                qualidade = qualidade.replace('PT PT','PT-PT')
			try:
				addDir('[B][COLOR green]' + urletitulo[0][1].replace('&#39;',"'") + '[/COLOR][/B][COLOR yellow] (' + ano + ')[/COLOR][COLOR red] (' + qualidade + ')[/COLOR]' + versao,urletitulo[0][0],73,thumbnail[0].replace('s1600','s320').replace('.gif','.jpg'),'','')
			except: pass
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco,73,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir("[B]Página Seguinte >>[/B]",proxima[0].replace('&amp;','&'),72,"",'','')
	except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_encontrar_videos_filmes(name,url):
        conta_id_video = 0
	addDir1(name,'','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = TFC_abrir_url(url)
        except: fonte = ''
        assist = re.findall('>ASSISTIR(.+?)</iframe>', fonte, re.DOTALL)
        fontes = re.findall("Clique aqui(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	if fonte:
                #-------------------- Videomega
                if '----------------------------<br />' in fonte and len(assist) > 1:
                        assistir_fontes = re.findall('>ASSISTIR(.*?)</iframe>', fonte, re.DOTALL)
                        for ass_fon in assistir_fontes:
                                match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)"').findall(ass_fon)
                                assis = re.compile('(.+?)</span>').findall(ass_fon)
                                conta_video = len(match)
                                if 'LEGENDADO' in assis[0]:
                                        addDir1('[COLOR blue]LEGENDADO:[/COLOR]','','',iconimage,False,'')
                                if 'PT/PT' in assis[0]:
                                        addDir1('[COLOR blue]AUDIO PT:[/COLOR]','','',iconimage,False,'')
                                addDir('[B]- Fonte 1 : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],70,iconimage,'','')
                else:        
                        match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)" .+?></iframe>').findall(fonte)
                        conta_video = len(match)
                        for url in match:                                
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],70,iconimage,'','')
                #-------------------------------
                #----------------- Not Videomega
		if numero_de_fontes > 0:
                        conta_video = 0
                        match = re.compile('<a href="(.+?)" .+? target=".+?">Clique aqui para ver!</a>').findall(fonte)
                        url = match[0]
                        if url != '':
                                try:
                                        for url in match:
                                                identifica_video = re.compile('=(.*)').findall(match[conta_video])
                                                id_video = identifica_video[0]
                                                conta_video = conta_video + 1
                                                conta_id_video = conta_id_video + 1
                                                TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video)
                                except:pass
                #-------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------    M18   -----------------------------------------------------------------#


                                
def TFC_encontrar_fontes_M18(url):
        url_m18 = 'http://www.blogger.com/blogin.g?blogspotURL=http://www.tuga-filmes.info/'
	html_m18 = TFC_abrir_url(url_m18)
	m18 = re.compile('<a class="maia-button maia-button-primary" href="http://www.tuga-filmes.info/(.+?)" target="_parent">').findall(html_m18)
	print m18
	url = 'http://www.tuga-filmes.info/search/label/Filmes' + m18[0]
	try:
		html_source = TFC_abrir_url(url)
	except: html_source = ''
	items = re.findall("<div id=\'titledata\'>(.*?)<br />", html_source, re.DOTALL)
	if items != []:
		print len(items)
		for item in items:
			urletitulo = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(item)
			thumbnail = re.compile('src="(.+?)"').findall(item)
			print urletitulo,thumbnail
			try:
				addDir(urletitulo[0][1].replace('&#8217;',"'"),urletitulo[0][0] + m18[0],82,thumbnail[0].replace('s72-c','s320'),'','')
			except: pass
	else:
		items = re.compile("<a href=\'(.+?)\' title=.+?>Assistir Online - </div>(.+?)<div id=\'player\'>").findall(html_source)
		for endereco,nome in items:
			addDir(nome.replace('&#8217;',"'"),endereco + m18[0],73,'','','')
	proxima = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(html_source)	
	try:
                addDir1('','','','',False,'')
		addDir('[B][COLOR red]Página Seguinte >>[/B][/COLOR]' + proxima[0].replace('amp;','') + m18[0],proxima[0].replace('amp;','') + m18[0],84,"",'','')
	except: pass

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFC_resolve_not_videomega_M18(name,url,id_video,conta_id_video):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link4=response.read()
        response.close()
        match = re.compile('<iframe frameborder="0" height="450" scrolling="no" src="(.+?)" .+?></iframe>').findall(link4)
        url=match[0]
        if "videomega" in url:
		try:
                        url = 'http://videomega.tv/iframe.php?ref=' + id_video
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "vidto.me" in url:
		try:
                        url = 'http://vidto.me/' + id_video + '.html'
                        print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Vidto.me)[/COLOR][/B]',url,70,iconimage,'','')
		except: pass
        if "dropvideo" in url:
		try:
                        url = 'http://dropvideo.com/embed/' + id_video
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](DropVideo)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
		except:pass
	if "streamin.to" in url:
                try:
                        url = 'http://streamin.to/embed-' + id_video + '.html'
			print url
			addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamin)[/COLOR][/B] [COLOR red]Não funciona[/COLOR]',url,70,iconimage,'','')
                except:pass                        
        if "putlocker" in url:
                try:
                        url = 'http://www.putlocker.com/embed/' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Putlocker)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	if "nowvideo" in url:
                try:
                        url = 'http://embed.nowvideo.sx/embed.php?v=' + id_video
                        print url
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Nowvideo)[/COLOR][/B]',url,70,iconimage,'','')
    		except:pass
    	return

#----------------------------------------------------------------------------------------------------------------------------------------------#

def TFC_encontrar_videos_M18(name,url):
        conta_id_video = 0
	addDir1('[B][COLOR blue]' + name + '[/COLOR][/B]','','',iconimage,False,'')
        addDir1('','','',iconimage,False,'')
        try:
                fonte = TFC_abrir_url(url)
        except: fonte = ''
        fontes = re.findall("Link Alternativo(.+?)", fonte, re.DOTALL)
        numero_de_fontes = len(fontes)
	try:
		link2=TFC_abrir_url(url)
	except: link2 = ''
	if link2:
                #-------------------- Videomega
                match = re.compile('<iframe .+? src="(.+?)" .+?></iframe>').findall(link2)
                conta_video = len(match)
		for url in match:
                        if "videomega" in match[0]:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Videomega)[/COLOR][/B]',match[0],70,iconimage,'','')
                        if "play.flashx" in match[0]:
                                conta_id_video = conta_id_video + 1
                                addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](FlashX)[/COLOR][/B]',match[0],70,iconimage,'','')
		if numero_de_fontes > 0:
                        conta_video = 0
                        match = re.compile('<a href="(.+?)">Link Alternativo</a>').findall(link2)
                        url = match[0]
                        conta_id_video = conta_id_video + 1
                        addDir('[B]- Fonte ' + str(conta_id_video) + ' : [COLOR yellow](Streamcloud)[/COLOR][/B]',url,70,iconimage,'','')

                #-------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#



def TFC_play_movie(url,name,iconimage,checker,fanart):
        if "streamcloud" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "flashx" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
        if "vidto.me" in url:
		try:
			sources = []
			hosted_media = urlresolver.HostedMediaFile(url)
			sources.append(hosted_media)
			source = urlresolver.choose_source(sources)
			if source: 
				url = source.resolve()
    			else: url = ''
		except: pass
	if "putlocker" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "nowvideo" in url:
                try:
                        sources = []
                        hosted_media = urlresolver.HostedMediaFile(url)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
                        if source: 
                                url = source.resolve()
                        else: url = ''
    		except:pass
    	if "videomega" in url:
		try:
			if "iframe" not in url:
				id_videomega = re.compile('ref=(.*)').findall(url)[0]
				iframe_url = 'http://videomega.tv/iframe.php?ref=' + id_videomega
			else: iframe_url = url
			print iframe_url
			link3 = TFC_abrir_url(iframe_url)
			match=re.compile('document.write\(unescape\("(.+?)"\)').findall(link3)
			print match
			tit=re.compile('<div id="title">&nbsp;&nbsp;&nbsp;(.+?)</div>').findall(link3)
			video_url_escape = urllib.unquote(match[0])
			match=re.compile('file: "(.+?)"').findall(video_url_escape)
			subtitle=re.compile('"file": "(.+?)"').findall(video_url_escape)
			if subtitle == []:
				checker = ''
				url = match[0]
			else:
				checker = subtitle[0]
				url = match[0]
		except: pass
	dp = xbmcgui.DialogProgress()
	dp.create("TugaFilmesTv",'A sincronizar vídeos e legendas')
	dp.update(0)
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage)))
	addLink('Voltar',url,'')
	dp.update(1, 'A reproduzir o filme.')
	if dp.iscanceled(): return
        dp.close()
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
	if checker == '' or checker == None: pass
	else: xbmcPlayer.setSubtitles(checker)

#----------------------------------------------------------------------------------------------------------------------------------------------#
	
def TFC_abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

#----------------------------------------------------------------------------------------------------------------------------------------------#
              
def TFC_get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

#----------------------------------------------------------------------------------------------------------------------------------------------#

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,checker,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&checker="+urllib.quote_plus(checker)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir1(name,url,mode,iconimage,folder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',artfolder + 'five_wall_color.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": checker } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok



def TFC_TextBoxes(url):
        texto = ''
        try:
                texto_url = TFC_abrir_url(url)
        except: texto_url = ''
        texto_items = re.compile('>(.+?)<').findall(texto_url)
        if texto_items != []:
                for linhas in texto_items:
                        texto = texto + linhas + '\n'
        texto = texto.replace('bbbbb','\n')
	texto = texto.replace('\xe7','ç')
	texto = texto.replace('\xf5','õ')	
	texto = texto.replace('\xe3','ã')		
	class TextBox():
		"""Thanks to BSTRDMKR for this code:)"""
		# constants
		WINDOW = 10147		
		CONTROL_LABEL = 1
		CONTROL_TEXTBOX = 5
		
		def __init__( self, *args, **kwargs):
			# activate the text viewer window
			xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
			# get window
			self.win = xbmcgui.Window( self.WINDOW )
			# give window time to initialize
			xbmc.sleep( 500 )
			self.setControls()

		def setControls( self ):
			# set heading
			self.win.getControl( self.CONTROL_LABEL ).setLabel('[COLOR brown]ChangeLog: [/COLOR][B][COLOR green]TUGA[/COLOR][COLOR yellow]-[/COLOR][COLOR red]FILMES[/COLOR][/B].com')
			self.win.getControl( self.CONTROL_TEXTBOX ).setText(texto)
			return
	TextBox()


	
#----------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------#


          
params=TFC_get_params()
url=None
name=None
mode=None
checker=None
iconimage=None
fanart=None

try: url=urllib.unquote_plus(params["url"])
except: pass

try: name=urllib.unquote_plus(params["name"])
except: pass

try: mode=int(params["mode"])
except: pass

try: checker=urllib.unquote_plus(params["checker"])
except: pass

try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

try: fanart=urllib.unquote_plus(params["fanart"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Checker: "+str(checker)
print "Iconimage: "+str(iconimage)


if mode==None or url==None or len(url)<1:
        print ""
        TFC_MenuPrincipal(artfolder)

elif mode == 70: print "", TFC_play_movie(url,name,iconimage,checker,fanart)
elif mode == 71: TFC_MenuPrincipal(artfolder)
elif mode == 72: TFC_encontrar_fontes_filmes(url)
elif mode == 73: TFC_encontrar_videos_filmes(name,url)
elif mode == 74: TFC_pesquisar_filmes()
elif mode == 75: TFC_resolve_videomega_filmes(url,conta_id_video)
elif mode == 76: TFC_resolve_not_videomega_filmes(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 77: TFC_Menu_Filmes(artfolder)
elif mode == 78: TFC_Menu_Filmes_Por_Categorias(artfolder)
elif mode == 79: TFC_Menu_Filmes_Top_10(artfolder)
elif mode == 80: TFC_Menu_Series(artfolder)
elif mode == 81: TFC_Menu_Filmes_Brevemente(artfolder)
elif mode == 82: TFC_encontrar_videos_M18(name,url)
elif mode == 83: TFC_resolve_not_videomega_M18(name,url,id_video,conta_id_video,nome_fonte_video)
elif mode == 84: TFC_encontrar_fontes_M18(url)
elif mode == 85: TFC_pesquisar_M18()
elif mode == 86: TFC_Link_M18(artfolder)
elif mode == 87: TFC_Menu_M18(url,artfolder)
elif mode == 88: TFC_ChangeLog()
elif mode == 89: TFC_TextBoxes(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

