/*
 * ******************************************************************************
 *  jquery.mb.components
 *  file: mbContainer.js
 *
 *  Copyright (c) 2001-2013. Matteo Bicocchi (Pupunzi);
 *  Open lab srl, Firenze - Italy
 *  email: matteo@open-lab.com
 *  site: 	http://pupunzi.com
 *  blog:	http://pupunzi.open-lab.com
 * 	http://open-lab.com
 *
 *  Licences: MIT, GPL
 *  http://www.opensource.org/licenses/mit-license.php
 *  http://www.gnu.org/licenses/gpl.html
 *
 *  last modified: 16/01/13 22.45
 *  *****************************************************************************
 */
(function(){if(!(8>jQuery.fn.jquery.split(".")[1])){jQuery.browser={};jQuery.browser.mozilla=!1;jQuery.browser.webkit=!1;jQuery.browser.opera=!1;jQuery.browser.msie=!1;var a=navigator.userAgent;jQuery.browser.name=navigator.appName;jQuery.browser.fullVersion=""+parseFloat(navigator.appVersion);jQuery.browser.majorVersion=parseInt(navigator.appVersion,10);var c,b;if(-1!=(b=a.indexOf("Opera"))){if(jQuery.browser.opera=!0,jQuery.browser.name="Opera",jQuery.browser.fullVersion=a.substring(b+6),-1!=(b= a.indexOf("Version")))jQuery.browser.fullVersion=a.substring(b+8)}else if(-1!=(b=a.indexOf("MSIE")))jQuery.browser.msie=!0,jQuery.browser.name="Microsoft Internet Explorer",jQuery.browser.fullVersion=a.substring(b+5);else if(-1!=(b=a.indexOf("Chrome")))jQuery.browser.webkit=!0,jQuery.browser.name="Chrome",jQuery.browser.fullVersion=a.substring(b+7);else if(-1!=(b=a.indexOf("Safari"))){if(jQuery.browser.webkit=!0,jQuery.browser.name="Safari",jQuery.browser.fullVersion=a.substring(b+7),-1!=(b=a.indexOf("Version")))jQuery.browser.fullVersion= a.substring(b+8)}else if(-1!=(b=a.indexOf("Firefox")))jQuery.browser.mozilla=!0,jQuery.browser.name="Firefox",jQuery.browser.fullVersion=a.substring(b+8);else if((c=a.lastIndexOf(" ")+1)<(b=a.lastIndexOf("/")))jQuery.browser.name=a.substring(c,b),jQuery.browser.fullVersion=a.substring(b+1),jQuery.browser.name.toLowerCase()==jQuery.browser.name.toUpperCase()&&(jQuery.browser.name=navigator.appName);if(-1!=(a=jQuery.browser.fullVersion.indexOf(";")))jQuery.browser.fullVersion=jQuery.browser.fullVersion.substring(0, a);if(-1!=(a=jQuery.browser.fullVersion.indexOf(" ")))jQuery.browser.fullVersion=jQuery.browser.fullVersion.substring(0,a);jQuery.browser.majorVersion=parseInt(""+jQuery.browser.fullVersion,10);isNaN(jQuery.browser.majorVersion)&&(jQuery.browser.fullVersion=""+parseFloat(navigator.appVersion),jQuery.browser.majorVersion=parseInt(navigator.appVersion,10));jQuery.browser.version=jQuery.browser.majorVersion}})(jQuery);

/*
 * Name:jquery.mb.containerPlus
 * Version: 2.6.0
 * dependencies: UI.core.js, UI.draggable.js, UI.resizable.js
 */

(function($){
	jQuery.fn.buildContainers = function (options){
		return this.each (function (){
			if ($(this).is("[inited=true]")) return;
			this.options = {
				containment:"document",
				elementsPath:"elements/",
				dockedIconDim:35,
				onCreate:function(o){},
				onCollapse:function(o){},
				onBeforeIconize:function(o){},
				onIconize:function(o){},
				onClose: function(o){},
				onBeforeClose: function(o){},
				onResize: function(o,w,h){},
				onDrag: function(o,x,y){},
				onRestore:function(o){},
				onMaximize:function(o){},
				onLoad:function(o){},
				onClick:function(o){},
				mantainOnWindow:true,
				collapseEffect:"slide", //or "fade"
				effectDuration:300,
				zIndexContext:"auto" // or your selector (ex: ".containerPlus")
			};

			$.extend (this.options, options);

			var el=this;
			if(!el.id) el.id= new Date().getMilliseconds();
			var container=$(this);

			$(window).resize(function(){
				if (container.get(0).options.mantainOnWindow){
					$.doOnWindowResize(el);
				}
			});

			container.attr("inited","true");
			container.attr("iconized","false");
			container.attr("collapsed","false");
			container.attr("closed","false");
//            container.attr("options",this.options);
//						container.get(0).options=this.options;

			if (!container.css("position")=="absolute")
				container.css({position: "relative"});

			if ($.metadata){
				$.metadata.setType("class");
				$.each(container.metadata(), function(key, data){
					container.attr(key,data)
				});
				if (container.attr("alwaysOnTop")) container.css("z-index",100000).addClass("alwaysOnTop");
			}

			this.options.skin=container.attr("skin");

			if(this.options.onCreate)
				this.options.onCreate(container);


			if (container.attr("rememberMe")=="true"){
				container.attr("width" , container.mb_getCookie("width")!=null? container.mb_getCookie("width"):container.attr("width") );
				container.attr("height", container.mb_getCookie("height")!=null? container.mb_getCookie("height"):container.attr("height") );
				container.attr("closed", container.mb_getCookie("closed")!=null? container.mb_getCookie("closed"):container.attr("closed") );
				container.attr("collapsed", container.mb_getCookie("collapsed")!=null? container.mb_getCookie("collapsed"):container.attr("collapsed") );
				container.attr("iconized", container.mb_getCookie("iconized")!=null? container.mb_getCookie("iconized"):container.attr("iconized") );
				container.css("left", container.mb_getCookie("x")!=null? container.mb_getCookie("x"):container.css("left") );
				container.css("top", container.mb_getCookie("y")!=null? container.mb_getCookie("y"):container.css("top") );
			}

			var isStructured= container.find(".mbcontainercontent").size()>0;
			if(!isStructured){
				var content= container.html();
				container.empty();
				var structure=''+
						'<div class="no '+this.options.skin+'"><div class="ne '+this.options.skin+'"><div class="n '+this.options.skin+'"></div></div>'+
						'<div class="o '+this.options.skin+'"><div class="e '+this.options.skin+'"><div class="c '+this.options.skin+'">'+
						'<div class="mbcontainercontent '+this.options.skin+'">'+content+'</div></div>' +
						'</div></div>'+
						'<div><div class="so '+this.options.skin+'"><div class="se '+this.options.skin+'"><div class="s '+this.options.skin+'"> </div></div></div>'+
						'</div></div>';
				container.html(structure);
			}
			if(container.attr("title")) container.find(".n:first").html("<span>"+container.attr("title")+"</span>");

			if (container.attr("content")){
				var data= container.attr("data")?container.attr("data"):"";
				container.mb_changeContainerContent(container.attr("content"),data);
			}

			container.addClass(this.options.skin);
			container.find(".n:first").attr("unselectable","on");
			if (!container.find(".n:first").html()) container.find(".n:first").html("&nbsp;");
			container.containerSetIcon(container.attr("icon"), this.options.elementsPath);
			if (container.attr("buttons")) container.containerSetButtons(container.attr("buttons"),this.options);
			container.css({width:"99.9%"});

			if (container.attr("width")){
				var cw= $.browser.msie? container.attr("width"):container.attr("width")+"px";
				container.css({width:cw});
			}

			if (container.attr("height")){
				container.find(".c:first , .mbcontainercontent:first").css("height",container.attr("height")-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight()));
				container.attr("height","");
				container.css({height:""});

			}else if ($.browser.safari){
				container.find(".mbcontainercontent:first").css("padding-bottom",5);
			}

			var nwh=$(window).height();
			if (container.outerHeight()>nwh)
				container.find(".c:first , .mbcontainercontent:first").css("height",(nwh-20)-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight()));

			if (container.hasClass("draggable")){
				var pos=container.css("position")=="static"?"absolute":container.css("position");
				container.css({position:pos, margin:0});
				container.find(".n:first").css({cursor:"move"});
				container.mb_bringToFront(this.options.zIndexContext);

				container.draggable({
					handle:".n:first",
					delay:0,
					start:function(){},
					stop:function(){
						if(this.options.onDrag) this.options.onDrag($(this),container.css("left"),container.css("top"));
						if (container.attr("rememberMe")){
							container.mb_setCookie("x",container.css("left"));
							container.mb_setCookie("y",container.css("top"));
						}
					}
				});
				if($.iPhone) container.find(".n:first").addTouch();
				if (container.attr("grid") || (container.attr("gridx") && container.attr("gridy"))){
					var grid= container.attr("grid")? [container.attr("grid"),container.attr("grid")]:[container.attr("gridx"),container.attr("gridy")];
					container.draggable('option', 'grid', grid);
				}

				container.on("mousedown",function(){
					$(this).mb_bringToFront(this.options.zIndexContext);
					if(this.options.onClick) {
						this.options.onClick(container);
					}
				});
			}
			if (this.options.onLoad) {
				this.options.onLoad(container);
			}
			if (container.hasClass("resizable")){
				container.containerResize();
			}
			if (container.attr("collapsed")=="true"){
				container.attr("collapsed","false");
				container.containerCollapse(this.options);
			}
			if (container.attr("iconized")=="true"){
				container.attr("iconized","false");
				container.containerIconize(this.options, true);
			}
			if (container.mb_getState('closed')){
				container.attr("closed","false");
				container.mb_close();
				return;
			}

			if(!$.browser.msie){
				container.css("opacity",0);
				container.css("visibility","visible");
				container.fadeTo(this.options.effectDuration,1);
			}else{
				container.css("visibility","visible");
			}
			container.adjastPos();
			container.setContainment();
		});
	};


	jQuery.fn.setContainment=function(){
		var container=$(this);
		var opt= container.get(0).options;
		var containment=opt.containment;
		if(opt.containment == "document"){
			var dH=($(document).height()-(container.outerHeight()+10));
			var dW=($(document).width()-(container.outerWidth()+10));
			containment= [0,0,dW,dH]; //[x1, y1, x2, y2]
		}
		if(container.is(".draggable") && opt.containment!=""){
			container.draggable('option', 'containment', containment);
		}

		return containment;
	};

	jQuery.fn.containerResize = function (){
		var container=$(this);
		var isDraggable=container.hasClass("draggable");
		var handles= container.attr("handles")?container.attr("handles"):"s";
		var aspectRatio= container.attr("aspectRatio")?container.attr("aspectRatio"):false;
		var minWidth= container.attr("minWidth")?container.attr("minWidth"):350;
		var minHeight= container.attr("minHeight")?container.attr("minHeight"):150;

		container.resizable({
			handles:isDraggable ? "":handles,
			aspectRatio:aspectRatio,
			minWidth: minWidth ,
			minHeight: minHeight,
			iframeFix:true,
			helper: "mbproxy",
			start:function(e,o){
				var elH= container.attr("containment")?container.parents().height():$(window).height()+$(window).scrollTop();
				var elW= container.attr("containment")?container.parents().width():$(window).width()+$(window).scrollLeft();

				var elPos= container.attr("containment")? container.position():container.offset();
				$(container).resizable('option', 'maxHeight',elH-(elPos.top+20));
				$(container).resizable('option', 'maxWidth',elW-(elPos.left+20));
				o.helper.mb_bringToFront();
			},
			stop:function(){
				var resCont= $(this);//$.browser.msie || Opera ?o.helper:
				var elHeight= resCont.outerHeight()-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight());
				container.find(".c:first , .mbcontainercontent:first").css({height: elHeight});
				if (!isDraggable && !container.attr("handles")){
					var elWidth=container.attr("width") && container.attr("width")>0 ?container.attr("width"):"99.9%";
					container.css({width: elWidth});
				}
				if(this.options.onResize) this.options.onResize(container,container.css('width'),container.css('height'));
				if (container.attr("rememberMe")){
					container.mb_setCookie("width",container.outerWidth());
					container.mb_setCookie("height",container.outerHeight());
				}
				container.setContainment();
			}
		});
		if (container.attr("resizeGrid") || (container.attr("resizeGridx") && container.attr("resizeGridy"))){
			var grid= container.attr("resizeGrid")? [container.attr("resizeGrid"),container.attr("resizeGrid")]:[container.attr("resizeGridx"),container.attr("resizeGridy")];
			container.resizable( "option", "grid", grid);
		}

		container.resizable('option', 'maxHeight', $("document").outerHeight()-(container.offset().top+container.outerHeight())-10);

		/*
		 *TO SOLVE UI CSS CONFLICT I REDEFINED A SPECIFIC CLASS FOR HANDLERS
		 */

		container.find(".ui-resizable-n").addClass("mb-resize").addClass("mb-resize-resizable-n");
		container.find(".ui-resizable-e").addClass("mb-resize").addClass("mb-resize-resizable-e");
		container.find(".ui-resizable-w").addClass("mb-resize").addClass("mb-resize-resizable-w");
		container.find(".ui-resizable-s").addClass("mb-resize").addClass("mb-resize-resizable-s");
		container.find(".ui-resizable-se").addClass("mb-resize").addClass("mb-resize-resizable-se");

	};

	jQuery.fn.containerSetIcon = function (icon,path){
		var container=$(this);
		if (icon && icon!="" ){
			container.find(".ne:first").prepend("<img class='icon' src='"+path+"icons/"+icon+"' style='position:absolute'/>");
			container.find(".n:first").css({paddingLeft:25});
		}else{
			container.find(".n:first").css({paddingLeft:0});
		}
	};

	jQuery.fn.containerEdit = function(opt)
	{
		var container=$(this);
		var opt= container.get(0).options;
		var el=container.get(0);
		if(el.options.onEdit) el.options.onEdit($(el));
		
	};
	
	jQuery.fn.containerSetButtons = function (buttons,opt){
		var container=$(this);
		if (!opt) opt=container.get(0).options;
		var path= opt.elementsPath;
		if (buttons !=""){
			var btn=buttons.split(",");
			container.find(".ne:first").append("<div class='buttonBar'></div>");
			
			container.find(".buttonBar:first").append("<img src='"+path+opt.skin+"/edit-4.png' class='editContainer' title='Edit'/>");
			container.find(".editContainer:first").on("click",function(){container.containerEdit(opt);});
			
			for (var i in btn){
				if (btn[i]=="c"){
					container.find(".buttonBar:first").append("<img src='"+path+opt.skin+"/close.png' class='close' title='Delete note'/>");
					container.find(".close:first").on("click",function(){
						container.mb_close();
					});
				}
				if (btn[i]=="m"){
					container.find(".buttonBar:first").append("<img src='"+path+opt.skin+"/min.png' class='collapsedContainer' title='Minimize Note'/>");
					container.find(".collapsedContainer:first").on("click",function(){container.containerCollapse(opt);});
					container.find(".n:first").on("dblclick",function(){container.containerCollapse(opt);});
				}
				//todo : introduce print container content
				if (btn[i]=="p"){
					container.find(".buttonBar:first").append("<img src='"+path+opt.skin+"/document-print-4.png' title='Print Note' class='printContainer'/>");
					container.find(".printContainer:first").on("click",function(){});
				}
				if (btn[i]=="i"){
					container.find(".buttonBar:first").append("<img src='"+path+opt.skin+"/iconize.png' class='iconizeContainer' title='Iconize'/>");
					container.find(".iconizeContainer:first").on("click",function(){container.containerIconize(opt);});
				}
				
				
			}
			
			var fadeOnClose=$.browser.mozilla || $.browser.safari;
			if (fadeOnClose) container.find(".buttonBar:first img")
					.css({opacity:.5, cursor:"pointer","mozUserSelect": "none", "khtmlUserSelect": "none"})
					.mouseover(function(){$(this).fadeTo(200,1);})
					.mouseout(function(){if (fadeOnClose)$(this).fadeTo(200,.5);});
			container.find(".buttonBar:first img").attr("unselectable","on");
		}
	};

	jQuery.fn.containerCollapse = function (opt){
		this.each (function () {
			var container=$(this);
			if (!opt) opt=this.options;

			//console.debug(opt);

			if (!container.mb_getState("collapsed")){
				container.attr("w" , container.outerWidth());
				container.attr("h" , container.outerHeight());
				if (opt.collapseEffect=="fade")
					container.find(".o:first").fadeOut(opt.effectDuration,function(){container.setContainment();});
				else{
					container.find(".icon:first").hide();
					container.find(".o:first").slideUp(opt.effectDuration,function(){});
					container.animate({height:container.find(".n:first").outerHeight()+container.find(".s:first").outerHeight()},opt.effectDuration,function(){container.find(".icon:first").show();container.setContainment();});
				}
				container.attr("collapsed","true");
				container.find(".collapsedContainer:first").attr("src",opt.elementsPath+opt.skin+"/max.png");
				if(container.hasClass("resizable")) container.resizable("disable");
				if (opt.onCollapse) opt.onCollapse(container);

			}else{
				if (opt.collapseEffect=="fade")
					container.find(".o:first").fadeIn(opt.effectDuration,function(){container.setContainment();});
				else{
					container.find(".o:first").slideDown(opt.effectDuration,function(){});
					container.find(".icon:first").hide();
					container.animate({
								height:container.attr("h")
							},
							opt.effectDuration,function(){
								container.find(".icon:first").show();
								container.css({height:""});
								container.setContainment();
							});
				}
				if (container.hasClass("resizable")) container.resizable("enable");
				container.attr("collapsed","false");
				container.find(".collapsedContainer:first").attr("src",opt.elementsPath+opt.skin+"/min.png");
				container.find(".mbcontainercontent:first").css("overflow","auto");
				if (opt.onMaximize) opt.onMaximize(container);
			}
			if (container.attr("rememberMe")) container.mb_setCookie("collapsed",container.mb_getState("collapsed"));
		});
	};

	jQuery.fn.containerIconize = function (opt,runCallback){
		var container=$(this);
		if (typeof runCallback=="undefined") runCallback=true;
		if (!opt) opt=container.get(0).options;
		return this.each (function (){
			if (opt.onBeforeIconize) opt.onBeforeIconize(container);
			container.attr("iconized","true");
			if(container.attr("collapsed")=="false"){
				container.attr("h",container.outerHeight());
				container.attr("h",!container.attr("height") && !container.css("height")?"": container.outerHeight() );
			}
			container.attr("w",container.attr("width") && container.attr("width")>0 ? (!container.hasClass("resizable")? container.attr("width"):container.width()):!container.attr("handles")?"99.9%":container.width());
			container.attr("t",container.css("top"));
			container.attr("l",container.css("left"));
			if(container.hasClass("resizable")) container.resizable("disable");
			var l=0;
			var t= container.css("top");
			var dockPlace= container;
			if (container.attr("dock")){
				dockPlace = $("#"+container.attr("dock"));
				var icns= dockPlace.find("img:visible").size();
				l=$("#"+container.attr("dock")).offset().left+(opt.dockedIconDim*icns);
				t=$("#"+container.attr("dock")).offset().top+(opt.dockedIconDim/2);
			}
			/*
			 ICONIZING CONTAINER
			 */
			var myTitle = container.find(".n:first").text();
			this.dockIcon= $("<div style='word-wrap:break-word;'><img src='"+opt.elementsPath+"icons/"
					+(container.attr("icon")?container.attr("icon"):"restore.png")
					+"' class='restoreContainer' width='"+opt.dockedIconDim+"'/><div style='width:60px;'>" + myTitle +"</div></div>").appendTo(dockPlace)
					.css("cursor","pointer")
					.hide()
					.attr("contTitle",container.find(".n:first").text())
					.on("click",function(){

						container.attr("iconized","false");
						if (container.is(".draggable"))
							container.css({top:$(this).offset().top, left:$(this).offset().left});
						else
							container.css({left:"auto",top:"auto"});
						container.show();
						if (!$.browser.msie) {
							container.find(".no:first").fadeIn("fast");
							if(container.attr("collapsed")=="false"){
								container.animate({
											height:container.attr("h"),
											width:container.attr("w"),
											left:container.attr("l"),
											top:container.attr("t")},
										opt.effectDuration,function(){
											container.find(".mbcontainercontent:first").css("overflow","auto");
											if(container.hasClass("draggable")) {
												container.mb_bringToFront(opt.zIndexContext);
											}
											container.css({height:""});
											if(opt.onRestore) opt.onRestore(container);
										});
							}else
								container.animate({height:"60px", width:container.attr("w"), left:container.attr("l"),top:container.attr("t")},opt.effectDuration);
						} else {
							container.find(".no:first").show();
							if(container.attr("collapsed")=="false"){
								container.css({height:container.attr("h"), width:container.attr("w"),left:container.attr("l"),top:container.attr("t")},opt.effectDuration);
								container.find(".c:first , .mbcontainercontent:first").css("height",container.attr("h")-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight()));
							}
							else
								container.css({height:"60px", width:container.attr("w"),left:container.attr("l"),top:container.attr("t")},opt.effectDuration);
							if(opt.onRestore) opt.onRestore(container);
						}
						if (container.hasClass("resizable") && container.attr("collapsed")=="false") container.resizable("enable");
						$(this).remove();
						if(container.hasClass("draggable")) container.mb_bringToFront(opt.zIndexContext);
						$(".iconLabel").remove();
						container.attr("restored", true);
						if (container.attr("rememberMe")){
							container.mb_setCookie("restored",container.mb_getState("restored"));
							container.mb_setCookie("closed", false);
							container.mb_setCookie("iconized", false);
							container.mb_setCookie("collapsed", false);
						}
						if (opt.mantainOnWindow) $.doOnWindowResize(container);
					})
					.on("mouseenter",function(){
						var label="<div class='iconLabel'>"+$(this).attr("contTitle")+"</div>";
						$("body").append(label);
						$(".iconLabel").hide().css({
							position:"absolute",
							top:$(this).offset().top-20,
							left:$(this).offset().left+15,
							opacity:.9
						}).fadeIn("slow").mb_bringToFront(opt.zIndexContext);
					})
					.on("mouseleave",function(){
						$(".iconLabel").fadeOut("fast",function(){$(this).remove();});
					});

			if (!$.browser.msie) {
				container.find(".mbcontainercontent:first").css("overflow","hidden");
				container.find(".no:first").slideUp("fast");
				container.animate({ height:opt.dockedIconDim, width:opt.dockedIconDim,left:l,top:t},opt.effectDuration,function(){
					$(this.dockIcon).show();
					if (container.attr("dock")) container.hide();
					if (opt.onIconize && runCallback) opt.onIconize(container);
				});
			}else{
				container.find(".no:first").hide();
				container.css({ height:opt.dockedIconDim, width:opt.dockedIconDim,left:l,top:t});
				$(this.dockIcon).show();
				if (container.attr("dock")) container.hide();
				if (opt.onIconize && runCallback) opt.onIconize(container);
			}
			if (container.attr("rememberMe")) container.mb_setCookie("iconized",container.mb_getState("iconized"));
		});
	};

	jQuery.fn.mb_resizeTo = function (h,w,anim){
		if (anim || anim==undefined) anim=200;
		else
			anim=0;
		var container=$(this);
		if(container.mb_getState('closed') || container.mb_getState('iconized') ){
			if (w) container.attr("w",w);
			if (h) container.attr("h",h);
			if (container.attr("rememberMe")){
				container.mb_setCookie("width",container.attr("w"));
				container.mb_setCookie("height",container.attr("h"));
			}
			return;
		}
		if (!w) w=container.outerWidth();
		if (!h) h=container.outerHeight();
		var elHeight= h-container.find(".n:first").outerHeight()-(container.find(".s:first").outerHeight());
		container.find(".c:first , .mbcontainercontent:first").animate({height: elHeight},anim);
		container.animate({"height":h,"width":w},anim,function(){
			container.adjastPos();
			var opt= container.get(0).options;
			if (opt.onResize) opt.onResize(container);
			if (container.attr("rememberMe")){
				container.mb_setCookie("width",container.outerWidth());
				container.mb_setCookie("height",container.outerHeight());
			}
		});
	};

	jQuery.fn.mb_iconize = function (){
		return this.each(function(){
			var container=$(this);
			var opt= container.get(0).options;
			var el=container.get(0);
			if (!container.mb_getState('closed')){
				if (container.mb_getState('iconized')){
					var icon=el.dockIcon;
					$(icon).click();
					container.mb_bringToFront(opt.zIndexContext);
				}else{
					container.containerIconize();
				}
			}
		});
	};

	jQuery.fn.mb_open = function (url,data){
		this.each(function(){
			var container=$(this);
			if (container.mb_getState('closed')){
				var opt= container.get(0).options;
				var t=Math.floor(container.attr("t"));
				var l=Math.floor(container.attr("l"));
				container.css({top:t+"px", left:l+"px"});
				var el=container.get(0);
				if (url){
					if (!data) data="";
					container.mb_changeContainerContent(url,data);
				}

				if (!$.browser.msie){
					container.css("opacity",0);
					container.css("visibility","visible");
					container.fadeTo(opt.effectDuration*2,1);
				} else {
					container.css("visibility","visible");
					container.show();
				}

				container.attr("closed","false");
				if (container.attr("rememberMe")){
					container.mb_setCookie("closed",false);
					container.mb_setCookie("restored",true);
				}

				container.mb_bringToFront(opt.zIndexContext);
				container.attr("restored", true);

				if(!container.mb_getState("collapsed")){
					container.mb_resizeTo(container.attr("h"),container.attr("w"),false);
				}
				if(el.options.onRestore) el.options.onRestore($(el));
			}
			return container;
		})
	};

	jQuery.fn.mb_close = function (){
		var el=$(this).get(0);
		var container=$(this);
		if (!container.mb_getState('closed') && !container.mb_getState('iconized')){
			if(el.options.onBeforeClose) el.options.onBeforeClose($(el));
			if(!container.mb_getState('collapsed')){
				container.attr("w",container.outerWidth());
				container.attr("h",container.outerHeight());
				container.attr("t",container.offset().top);
				container.attr("l",container.offset().left);
			}
			if (container.attr("rememberMe")) container.mb_setCookie("closed",true);
			if (!$.browser.msie)
				container.fadeOut(300,function(){if(el.options.onClose) el.options.onClose($(el));});
			else {
				container.hide();
				if(el.options.onClose) el.options.onClose($(el));
			}
			container.attr("closed","true");
		}
		return $(this);
	};

	jQuery.fn.mb_toggle = function (){
		if (!$(this).mb_getState('closed') && !$(this).mb_getState('iconized')){
			$(this).containerCollapse();
		}
		return $(this);
	};

	jQuery.fn.mb_changeContent= function(url, data){
		var where=$(this);
		if (!data) data="";
		$.ajax({
			type: "POST",
			url: url,
			data: data,
			dataType:"html",
			success: function(html){
				where.html(html);
			}
		});
	};

	jQuery.fn.mb_expand=function(path){
		if($(this).mb_getState('closed'))
			$(this).mb_open();
		if(!$(this).mb_getState('iconized')) return;
		if(path)
			$(this).mb_changeContainerContent(path);

		$(this).mb_iconize();
	};


	jQuery.fn.mb_changeContainerContent=function(url, data){
		$(this).find(".mbcontainercontent:first").mb_changeContent(url,data);
	};

	jQuery.fn.mb_getState= function(attr){
		var state = $(this).attr(attr);
		state= state == "true";
		return state;
	};

	jQuery.fn.mb_fullscreen= function(){
		var container=$(this);
		var opt= container.get(0).options;
		if (container.mb_getState('iconized') || container.mb_getState('collapsed') || container.mb_getState('closed')){
			container.attr("w",$(window).width()-40);
			container.attr("h",$(window).height()-40);
			container.attr("t",20);
			container.attr("l",20);
			container.css("height","");
			return;
		}
		container.animate({top:20,left:20, position:"relative"},200, function(){
			if (container.attr("rememberMe")){
				container.mb_setCookie("x",$(this).css("left"));
				container.mb_setCookie("y",$(this).css("top"));
			}
		});
		container.mb_resizeTo($(window).height()-40,$(window).width()-40);

		container.attr("w",$(this).outerWidth());
		container.attr("h",$(this).outerHeight());
		container.attr("t",$(this).offset().top);
		container.attr("l",$(this).offset().left);
		container.css("height","");
		container.mb_bringToFront(opt.zIndexContext);
		return container;
	};

	jQuery.fn.mb_centerOnWindow=function(anim){
		var container=$(this);
		var nww=$(window).width();
		var nwh=$(window).height();
		var ow=container.attr("w")?container.attr("w"):container.outerWidth();
		var oh= container.attr("h")?container.attr("h"):container.outerHeight();
		var l= (nww-ow)/2;
		var t= ((nwh-oh)/2)>0?(nwh-oh)/2:10;
		if (container.css("position")!="fixed"){
			$(this).css("position","absolute");
			l=l+$(window).scrollLeft();
			t=t+$(window).scrollTop();
		}
		if (anim)
			container.animate({top:t,left:l},300,function(){
				if (container.attr("rememberMe")){
					container.mb_setCookie("x",$(this).css("left"));
					container.mb_setCookie("y",$(this).css("top"));
				}
			});
		else{
			container.css({top:t,left:l});
			if (container.attr("rememberMe")){
				container.mb_setCookie("x",$(this).css("left"));
				container.mb_setCookie("y",$(this).css("top"));
			}
		}
		container.attr("t",t);
		container.attr("l",l);
		return container;
	};

	jQuery.fn.mb_switchFixedPosition=function(){
		return this.each(function(){
			var container=$(this);
			if(typeof container.attr("pos") == "undefined")
				container.attr("pos", container.css("position"));
			if(container.css("position") == container.attr("pos")){
				container.css("top", parseFloat(container.css("top"))-$(window).scrollTop());
				container.css("position","fixed");
			} else{
				container.css("position",container.attr("pos"));
				container.css("top", parseFloat(container.css("top"))+$(window).scrollTop());
			}
		});
	};
	jQuery.fn.mb_switchAlwaisOnTop=function(){
		return this.each(function(){
			var container=$(this);
			if (!container.hasClass("alwaysOnTop")){
				container.get(0).zi=container.css("z-index");
				container.css("z-index",100000).addClass("alwaysOnTop");
			}else{
				container.removeClass("alwaysOnTop").css("z-index",container.get(0).zi);
			}
		});
	};

	jQuery.fn.mb_setPosition=function(top,left){
		return this.each(function(){
			var container=$(this);
			container.animate({top:top, left:left},300);
		});
	};

	jQuery.fn.mb_bringToFront= function(zIndexContext){
		var zi=10;
		var els= zIndexContext && zIndexContext!="auto" ? $(zIndexContext):$("*");
		els.not(".alwaysOnTop").each(function() {
			if($(this).css("position")=="absolute" || $(this).css("position")=="fixed"){
				var cur = parseInt($(this).css('zIndex'));
				zi = cur > zi ? parseInt($(this).css('zIndex')) : zi;
			}
		});
		$(this).not(".alwaysOnTop").css('zIndex',zi+=1);
		return zi;
	};

	//MANAGE WINDOWS POSITION ONRESIZE
	var winw=$(window).width();
	var winh=$(window).height();


	$.doOnWindowResize=function(el){
		clearTimeout(el.doRes);
		el.doRes=setTimeout(function(){
			winw=$(window).width();
			winh=$(window).height();
			$(el).adjastPos();
		},400);
	};

	$.fn.adjastPos= function(margin){
		var container=$(this);
		var opt=container.get(0).options;
		if (!opt.mantainOnWindow) return;
		if(!margin) margin=20;
		var nww=$(window).width()+$(window).scrollLeft();
		var nwh=$(window).height()+$(window).scrollTop();
		this.each(function(){
			var left=container.offset().left, top=container.offset().top;
			if ((left+container.outerWidth())>nww || top+container.outerHeight()>nwh || left<0 || top<0){
				var l=(container.offset().left+container.outerWidth())>nww ? nww-container.outerWidth()-margin: container.offset().left<0? margin: container.offset().left;
				var t= (container.offset().top+container.outerHeight())>nwh ? nwh-container.outerHeight()-margin: container.offset().top<0 ?margin: container.offset().top;
				container.animate({left:l, top:t},550,function(){
					container.setContainment();
				});
			}
			container.setContainment();
		});
	};

	//COOKIES
	jQuery.fn.mb_setCookie = function(name,value,days) {
		var id=$(this).attr("id");
		if(!id) id="";
		if (!days) days=7;
		var date = new Date(), expires;
		date.setTime(date.getTime()+(days*24*60*60*1000));
		expires = "; expires="+date.toGMTString();
		document.cookie = name+"_"+id+"="+value+expires+"; path=/";
	};

	jQuery.fn.mb_getCookie = function(name) {
		var id=$(this).attr("id");
		if(!id) id="";
		var nameEQ = name+"_"+id + "=";
		var ca = document.cookie.split(';');
		for(var i=0;i < ca.length;i++) {
			var c = ca[i];
			while (c.charAt(0)==' ') c = c.substring(1,c.length);
			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
		}
		return null;
	};

	jQuery.fn.mb_removeCookie = function(name) {
		$(this).mb_setCookie(name,"",-1);
	};

})(jQuery);
