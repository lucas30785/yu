# -*- coding: utf-8 -*-
import io

content = """#EXTM3U url-tvg="https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/claro.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/globo.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/vivoplay.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/maissbt.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/plutotv.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/xsports.xml,https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz" tvg-shift=-3 x-tvg-url="https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/claro.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/globo.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/vivoplay.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/maissbt.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/plutotv.xml,https://raw.githubusercontent.com/limaalef/BrazilTVEPG/main/xsports.xml,https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz"

#EXTINF:-1 tvg-id="TV Nova Nordeste" tvg-logo="https://tvnova.tv.br/wp-content/webp-express/webp-images/uploads/2023/03/Logo_TV_NOVA.png.webp" group-title="PE",TV Nova Nordeste
https://acesso.ecast.site:3675/live/novatvlive.m3u8

#EXTINF:-1 tvg-id="XSports" tvg-name="X Sports FHD" tvg-logo="https://imgmxa.net/xsports.png" group-title="ESPORTE",X Sports FHD
http://opbrasil.top:80/2leh34732/11974534732/148838.ts

#EXTINF:-1 tvg-id="XSports" tvg-name="X Sports FHD [H265]" tvg-logo="https://imgmxa.net/xsports.png" group-title="ESPORTE",X Sports FHD [H265]
http://opbrasil.top:80/2leh34732/11974534732/148839.ts

#EXTINF:-1 tvg-id="XSports" tvg-name="X Sports HD" tvg-logo="https://imgmxa.net/xsports.png" group-title="ESPORTE",X Sports HD
http://opbrasil.top:80/2leh34732/11974534732/148837.ts

#EXTINF:-1 tvg-id="XSports" tvg-name="X Sports SD" tvg-logo="https://imgmxa.net/xsports.png" group-title="ESPORTE",X Sports SD
http://opbrasil.top:80/2leh34732/11974534732/148836.ts

#EXTINF:-1 tvg-id="SBT" tvg-name="SBT TV Jornal Recife HD" tvg-logo="https://imgmxa.net/sbt.png" group-title="Canais PE",SBT TV Jornal Recife HD
http://opbrasil.top:80/2leh34732/11974534732/81866.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Asa Branca FHD" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",GB Asa Branca FHD
http://opbrasil.top:80/2leh34732/11974534732/671.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Asa Branca HD" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",GB Asa Branca HD
http://opbrasil.top:80/2leh34732/11974534732/670.ts

#EXTINF:-1 tvg-id="Record" tvg-name="Record Recife HD" tvg-logo="https://imgmxa.net/record.png" group-title="PE",Record Recife HD
http://opbrasil.top:80/2leh34732/11974534732/204656.ts

#EXTINF:-1 tvg-id="Record" tvg-name="Record Recife SD" tvg-logo="https://imgmxa.net/record.png" group-title="PE",Record Recife SD
http://opbrasil.top:80/2leh34732/11974534732/204655.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Nordeste Recife FHD" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",Globo Nordeste
http://opbrasil.top:80/2leh34732/11974534732/556.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Nordeste Recife FHD [Alt]" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",GGlobo Nordeste
http://opbrasil.top:80/2leh34732/11974534732/81631.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Nordeste Recife HD" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",Globo Nordeste
http://opbrasil.top:80/2leh34732/11974534732/557.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Nordeste Recife HD [Alt]" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",Globo Nordeste
http://opbrasil.top:80/2leh34732/11974534732/81632.ts

#EXTINF:-1 tvg-id="Globo Nordeste" tvg-name="GB Nordeste Recife SD" tvg-logo="https://imgmxa.net/globo-2023.png" group-title="PE",Globo Nordeste
http://opbrasil.top:80/2leh34732/11974534732/168.ts

#EXTINF:-1 tvg-id="TV Vitória" tvg-logo="https://www.tvvitoriape.com.br/public/20568-2024-06-10.jpg" group-title="PE",TV Vitoria
https://5c483b9d1019c.streamlock.net/tvvitoriape/tvvitoriape/playlist.m3u8

#EXTINF:-1 tvg-id="TVU" tvg-logo="https://upload.wikimedia.org/wikipedia/pt/thumb/a/a7/Logotipo_da_TV_Universit%C3%A1ria_%28Recife%29.png/500px-Logotipo_da_TV_Universit%C3%A1ria_%28Recife%29.png" group-title="PE",TVU
http://150.161.93.220/hls/index.m3u8

#EXTINF:-1 tvg-id="TV Evangelizar" tvg-logo="https://tvevangelizar.com.br/wp-content/themes/tvevangelizar/assets/img/home/logo-topx.png" group-title="Catolico",TV Evangelizar
https://tvevangelizar.brasilstream.com.br/hls/tvevangelizar/index.m3u8

#EXTINF:-1 tvg-id="Rede Vida" tvg-logo="https://redevida.com.br/wp-content/uploads/2024/07/logo-redevida.png.webp" group-title="Catolico",Rede Vida
https://d12e4o88jd8gex.cloudfront.net/out/v1/cea3de0b76ac4e82ab8ee0fd3f17ce12/index.m3u8

#EXTINF:-1 tvg-id="TV Aparecida" tvg-logo="https://upload.wikimedia.org/wikipedia/pt/thumb/1/1e/Logotipo_da_TV_Aparecida.png/330px-Logotipo_da_TV_Aparecida.png" group-title="Catolico",TV Aparecida
https://cdn.jmvstream.com/w/LVW-9716/LVW9716_HbtQtezcaw/playlist.m3u8

#EXTINF:-1 tvg-id="Rede Século 21" tvg-logo="https://back.ww-cdn.com/superstatic/version/1821384/iphone/1021/photo/root_grid_header_elements_149071185995_image@iphone6plus.png?v=1714054908&force_webp=1" group-title="Catolico",Rede Século 21
https://cdn.live.br1.jmvstream.com/w/LVW-19954/LVW19954_V2nXt9iI2m/playlist.m3u8

#EXTINF:-1 tvg-id="TV Pai Eterno" tvg-logo="https://upload.wikimedia.org/wikipedia/pt/thumb/7/7c/Logotipo_TV_Pai_Eterno.png/330px-Logotipo_TV_Pai_Eterno.png" group-title="Catolico",TV Pai Eterno
https://video09.logicahost.com.br/paieterno/paieterno/playlist.m3u8

#EXTINF:-1 tvg-id="TV Horizonte" tvg-logo="https://tvhorizonte.com.br/wp-content/uploads/2024/12/logo-rede-catedral.png" group-title="Catolico",TV Horizonte
https://tvhorizonte.brasilstream.com.br/hls/tvhorizonte/index.m3u8

#EXTINF:-1 tvg-id="TV Imaculada" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LOGO_TV_2019.png/1200px-LOGO_TV_2019.png" group-title="Catolico",Tv Imaculada
https://video08.logicahost.com.br/redeimaculada/redeimaculada/playlist.m3u8

#EXTINF:-1 tvg-id="Canção Nova" tvg-logo="https://upload.wikimedia.org/wikipedia/pt/thumb/3/3f/Logotipo_da_TV_Can%C3%A7%C3%A3o_Nova.png/330px-Logotipo_da_TV_Can%C3%A7%C3%A3o_Nova.png" group-title="Catolico",TV Canção Nova HD
https://gerenciar.vivatele.com:443/viva_padrao/viva2384/5

#EXTINF:-1 tvg-id="Canção Nova" tvg-logo="https://static.cancaonova.com/images/app_tv_icon.png" group-title="Catolico",TV Canção Nova Portugal
https://5c65286fc6ace.streamlock.net/cancaonova/CancaoNova.stream_720p/playlist.m3u8

#EXTINF:-1 tvg-id="Katholika" tvg-logo="https://katholika.com/wp-content/uploads/elementor/thumbs/logo_katholika_branco-800px-qdtntsst8kjm20lqglp5vqxivrr9mce9bxh2npxd5y.png" group-title="Catolico",Katholika
https://acesso.ecast.site:3743/live/katholikalive.m3u8

#EXTINF:-1 tvg-id="SBT" tvg-logo="https://imgur.com/KO1v3pS.png" group-title="ABERTO",SBT São Paulo
https://cdn.live.br1.jmvstream.com/w/LVW-10801/LVW10801_Xvg4R0u57n/playlist.m3u8

#EXTINF:-1 tvg-id="Record" tvg-logo="https://upload.wikimedia.org/wikipedia/pt/thumb/0/0e/Logotipo_da_Record_%28rede_de_televis%C3%A3o%29.png/330px-Logotipo_da_Record_%28rede_de_televis%C3%A3o%29.png" group-title="ABERTO",Record
https://video08.logicahost.com.br/portaldatropical02/portaldatropical02/playlist.m3u8

#EXTINF:-1 tvg-id="Band" tvg-logo="https://imgur.com/P3Ldnvp.png" group-title="ABERTO",BAND HD
https://5b7f3c45ab7c2.streamlock.net/arapuan/ngrp:arapuan_all/playlist.m3u8

#EXTINF:-1 tvg-id="TV Cultura" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Cultura_logo_2013.svg/330px-Cultura_logo_2013.svg.png" group-title="ABERTO",CULTURA HD
https://player-tvcultura.stream.uol.com.br/live/tvcultura.m3u8

#EXTINF:-1 tvg-id="TV Brasil" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/TV_Brasil_logo_2023.svg/330px-TV_Brasil_logo_2023.svg.png" group-title="ABERTO",TV BRASIL
https://tvbrasil-stream.ebc.com.br/index.m3u8

#EXTINF:-1 tvg-id="RedeTV!" tvg-logo="https://imgur.com/2vYqKX5.png" group-title="ABERTO",REDE TV
https://5b7f3c45ab7c2.streamlock.net/arapuan/ngrp:arapuan_all/playlist.m3u8

#EXTINF:-1 tvg-id="Play TV" tvg-logo="https://playtv.com.br/site/wp-content/uploads/2023/07/PlayTV-logo-pequeno-e1700746282386.png" group-title="ABERTO",PlayTV
https://isaocorp.cloudecast.com/playtv/mono.m3u8

#EXTINF:-1 tvg-id="Cazé TV" tvg-logo="https://upload.wikimedia.org/wikipedia/pt/2/22/Logotipo_da_Caz%C3%A9TV.png" group-title="ESPORTE",Cazé TV
https://dfr80qz435crc.cloudfront.net/MNOP/Amagi/Caze/Caze_TV_BR/Caze_TV.m3u8

#EXTINF:-1 tvg-id="ge.globo" tvg-logo="https://yt3.googleusercontent.com/dc3tNE8gU99pZ_5gPcl_7U-hKf_Zzguxa4wTSexNKVNAWxli7hblw2BsrdHWASnjXRWciqecfTk=s160-c-k-c0x00ffffff-no-rj" group-title="ESPORTE",GE TV
https://dfr80qz435crc.cloudfront.net/EFGH/Amagi/Globo/GE_Fast_BR/GE_Fast.m3u8

#EXTINF:-1 tvg-id="NSports" tvg-logo="https://www.cxtv.com.br/img/Tvs/Logo/webp-m/8bbe6817af0af2e0e5a6df96f245b752.webp" group-title="ESPORTE",N SPORT
https://ogc-nsprt-tcl-roku-syndication.otteravision.com/ogc/nsprt/nsprt_720p.m3u8

#EXTINF:-1 tvg-id="Times Brasil" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Times_Brasil_CNBC_logo.svg/330px-Times_Brasil_CNBC_logo.svg.png" group-title="Jornalismo",TIMES | Exclusivo CNBC
https://f593663c.wurl.com/master/f36d25e7e52f1ba8d7e56eb859c636563214f541/TEctYnJfVGltZXNCcmFzaWxsaWNlbmNpYWRvZXhjbHVzaXZvQ05CQ19ITFM/playlist.m3u8

#EXTINF:-1 tvg-id="Jovem Pan News" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/9/9d/Jovem_Pan_News.png" group-title="Jornalismo",JOVEM PAN NEWS
https://d6yfbj4xxtrod.cloudfront.net/out/v1/7836eb391ec24452b149f3dc6df15bbd/index.m3u8

#EXTINF:-1 tvg-id="SBT News" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/SBT_News_2025.svg/500px-SBT_News_2025.svg.png" group-title="Jornalismo",SBT NEWS
https://amg00527-amg00527c5-amgplt0026.playout.now3.amagi.tv/ts-us-w2-n1/playlist/amg00527-amg00527c5-amgplt0026/playlist.m3u8

#EXTINF:-1 tvg-id="Record News" tvg-logo="https://images.pluto.tv/channels/6102e04e9ab1db0007a980a1/colorLogoPNG.png" group-title="Jornalismo",Record News
https://rnw-rn-samsungtvplus.otteravision.com/rnw/rn/rnw_rn.m3u8

#EXTINF:-1 tvg-id="CNN Brasil" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/CNN_Brasil.svg/330px-CNN_Brasil.svg.png" group-title="Jornalismo",CNN Brasil
https://d25usgadhphvwi.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-y4riz7eo92zpm/hls/main.m3u8

#EXTINF:-1 tvg-id="Canal UOL" tvg-logo="https://nxplay-images.comets.com.br/resize/67d58f13da035_3dff5fc0864d0fbd7d22085e1256fd30.png" group-title="Jornalismo",Canal UOL
https://ssai2-ads.api.leiniao.com/global-adinsertion-api/hls/live/v2/d2e9f2169fab45528fa125f7b2d55927/playlist.m3u8

#EXTINF:-1 tvg-id="BM&C News" tvg-logo="https://imgur.com/eqL0AHD.png" group-title="Jornalismo",bmandc-news
https://jmp2.uk/plu-666c9c60a7efd40008f552f0.m3u8

#EXTINF:-1 tvg-id="TVD News" tvg-logo="https://tvdnews.com.br/wp-content/uploads/2025/03/lg-tvd043324-300x169.png" group-title="Jornalismo",TVD News
http://201.159.95.110:25461/live/site/site/666.m3u8

#EXTINF:-1 channel-id="66a01dcb8561260008b0a41d" tvg-id="66a01dcb8561260008b0a41d" tvg-chno="1503" tvg-name="MTV Classic" tvg-logo="https://images.pluto.tv/channels/66a01dcb8561260008b0a41d/colorLogoPNG.png" group-title="PLUTO",MTV Classic
https://stitcher-ipv4.pluto.tv/v1/stitch/embed/hls/channel/66a01dcb8561260008b0a41d/master.m3u8?CreatedWithS2by=Neywerson&country=BR&deviceType=samsung-tvplus&deviceMake=samsung&deviceModel=samsung&deviceVersion=unknown&appVersion=unknown&deviceLat=0&deviceLon=0&deviceDNT=%7BTAROPT%7D&deviceId=%7BPSID%7D&advertisingId=%7BPSID%7D&us_privacy=1YNY&samsung_app_domain=%7BAPP_DOMAIN%7D&samsung_app_name=%7BAPP_NAME%7D&profileLimit=&profileFloor=&embedPartner=samsung-tvplus&profilesFromStream=true

#EXTINF:-1 tvg-id="MTV Biggest Pop" tvg-name="MTV Biggest Pop" tvg-logo="https://imgur.com/8uGhB6m.png" group-title="PLUTO",MTV Biggest Pop
http://service-stitcher.clusters.pluto.tv/stitch/hls/channel/6047fbdbbb776a0007e7f2ff/master.m3u8?advertisingId=&appName=web&appVersion=unknown&appStoreUrl=&architecture=&buildVersion=&clientTime=0&deviceDNT=0&deviceId=65aa3200-f9bd-11eb-8aa4-9fbe6c9efd24&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&sid=93901adb-1cd6-4054-9f35-6f3746b30848&userId=&serverSideAds=true

#EXTINF:-1 channel-id="5f121460b73ac6000719fbaf" tvg-id="5f121460b73ac6000719fbaf" tvg-chno="1402" tvg-name="Nick Jr. Club" tvg-logo="https://images.pluto.tv/channels/5f121460b73ac6000719fbaf/colorLogoPNG.png" group-title="PLUTO",Nick Jr. Club
https://stitcher-ipv4.pluto.tv/v1/stitch/embed/hls/channel/5f121460b73ac6000719fbaf/master.m3u8?CreatedWithS2by=Neywerson&country=BR&deviceType=samsung-tvplus&deviceMake=samsung&deviceModel=samsung&deviceVersion=unknown&appVersion=unknown&deviceLat=0&deviceLon=0&deviceDNT=%7BTAROPT%7D&deviceId=%7BPSID%7D&advertisingId=%7BPSID%7D&us_privacy=1YNY&samsung_app_domain=%7BAPP_DOMAIN%7D&samsung_app_name=%7BAPP_NAME%7D&profileLimit=&profileFloor=&embedPartner=samsung-tvplus&profilesFromStream=true

#EXTINF:-1 channel-id="5f12151794c1800007a8ae63" tvg-id="5f12151794c1800007a8ae63" tvg-chno="1440" tvg-name="Nickelodeon Clássico" tvg-logo="https://images.pluto.tv/channels/5f12151794c1800007a8ae63/colorLogoPNG.png" group-title="PLUTO",Nickelodeon Clássico
https://stitcher-ipv4.pluto.tv/v1/stitch/embed/hls/channel/5f12151794c1800007a8ae63/master.m3u8?CreatedWithS2by=Neywerson&country=BR&deviceType=samsung-tvplus&deviceMake=samsung&deviceModel=samsung&deviceVersion=unknown&appVersion=unknown&deviceLat=0&deviceLon=0&deviceDNT=%7BTAROPT%7D&deviceId=%7BPSID%7D&advertisingId=%7BPSID%7D&us_privacy=1YNY&samsung_app_domain=%7BAPP_DOMAIN%7D&samsung_app_name=%7BAPP_NAME%7D&profileLimit=&profileFloor=&embedPartner=samsung-tvplus&profilesFromStream=true

#EXTINF:-1 tvg-id="638f2e6c7a07960007e52913" tvg-logo="https://images.pluto.tv/channels/638f2e6c7a07960007e52913/colorLogoPNG.png" group-title="PLUTO",MTV Love Music
http://stitcher-ipv4.pluto.tv/v1/stitch/embed/hls/channel/638f2e6c7a07960007e52913/master.m3u8?deviceType=samsung-tvplus&deviceMake=samsung&deviceModel=samsung&deviceVersion=unknown&appVersion=unknown&deviceLat=0&deviceLon=0&deviceDNT=%7BTARGETOPT%7D&deviceId=%7BPSID%7D&advertisingId=%7BPSID%7D&us_privacy=1YNY&samsung_app_domain=%7BAPP_DOMAIN%7D&samsung_app_name=%7BAPP_NAME%7D&profileLimit=&profileFloor=&embedPartner=samsung-tvplus

#EXTINF:-1 tvg-id="Melphis TV" tvg-logo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKSWZbbW379L1HqdgaddxSDx6ZDrtNL_lQQw&s" group-title="ABERTO",Melphis TV
https://srv2.zcast.com.br/melphistv/melphistv/playlist.m3u8

#EXTINF:-1 tvg-id="Trace Latina" tvg-logo="https://www.cxtv.com.br/img/Tvs/Logo/webp-l/5536c18c8dc6b2ee955e65c59720b9c3.webp" group-title="PLUTO",Trace Latina
https://ssai2-ads.api.leiniao.com/global-adinsertion-api/hls/live/pipAd/692b462f15854a7fbeb7672ebcd14a04/playlist.m3u8

#EXTINF:-1 tvg-id="Trace Brazuca" tvg-logo="https://www.cxtv.com.br/img/Tvs/Logo/webp-l/6983af07687a9604b1142c1967f5bcbc.webp" group-title="PLUTO",Trace Brazuca
https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00520-tcl-tracebrazuca-tcl/playlist.m3u8

#EXTINF:-1 tvg-id="Trace Urban" tvg-logo="https://www.cxtv.com.br/img/Tvs/Logo/webp-l/74a76057b28ccd9c9d48045b64825ff9.webp" group-title="PLUTO",Trace Urban
https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg00520-tcl-traceurban-tcl/playlist.m3u8
"""

with io.open("C:\\Users\\lm262\\OneDrive\\Área de Trabalho\\programacao\\IPTV\\playlist_base.m3u", "w", encoding="utf-8") as f:
    f.write(content)
