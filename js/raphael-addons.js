Raphael.fn.arc=function(a,t,h,i,n,r,c){var e=[n,r,c,0,1,h,i].join(" ");return this.path("M"+a+" "+t+" a "+e)},Raphael.fn.circularArc=function(a,t,h,i,n){var r=a+h*Math.cos(i*Math.PI/180),c=t+h*Math.sin(i*Math.PI/180),e=a+h*Math.cos(n*Math.PI/180),M=t+h*Math.sin(n*Math.PI/180);return this.arc(r,c,e-r,M-c,h,h,0)},Raphael.fn.scaleText=function(a,t,h,i,n){for(var r=a.getBBox(),c=1,e=r.width,M=r.height;e>t||M>h;)c-=.01,e=r.width*c,M=r.height*c;e=r.width*c,M=r.height*c,a.scale(c,c,i,n)};