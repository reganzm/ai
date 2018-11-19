/* 算薪资 */
var Calculator = (function( $ , undefined ){
    var Degree = {
            'bk' : '本科' ,
            'bs' : '博士' ,
            'ss' : '硕士' ,
            'zk' : '专科' 
        },
        gender = { 
            'man' : '男',
            'woman' : '女'
        },
        JobType = {
            'cp' : '产品狗',
            'gcs' : '攻城狮',
            'sj' : '射鸡湿',
            'yy' : '运营人猿',
            'sc' : '市场商务',
            'xz' : '暖心行政'
        },
        SecondClass = {
            'gcs': {
                'C/C++': 'C/C++',
                'C#': 'C#',
                'Java': 'Java',
                'Python': 'Python',
                'PHP': 'PHP',
                'JavaScript': 'JavaScript',
                'Android': 'Android',
                'iOS': 'iOS',
                'qd': '前端',
                'hd': '后端',
                'ce': '测试',
                'yw': '运维',
                'xmjl': '项目经理',
                'jgs': '架构师',
                'zj': '总监'
            },
            'xz': {
                'xz': '行政',
                'rs': '人事',
                'cw': '财务',
                'kf': '客服',
                'zj': '总监/经理',
                'zl': '助理'
            },
            'sj': {
                'sjsj': '视觉设计',
                'jxsj': '交互设计',
                'pmsj': '平面设计',
                'yxms': '游戏美术',
                'dh': '动画',
                'yh': '原画',
                'yy': '用研',
                'UI': 'UI',
                'UE': 'UE',
                'WEB': 'WEB',
                'APP': 'APP',
                'zj': '总监'
            },
            'cp': {
                'cpjl': '产品经理',
                'cpzj': '产品总监',
                'cpzl': '产品助理'
            },
            'sc': {
                'xs': '销售',
                'sctg': '市场推广',
                'zj': ' 总监'
            },
            'yy': {
                'yyzy': '运营专员',
                'yyzj': '运营总监',
                'bj': '编辑',
                'zb': '主编'
            }
        },
        City = {
            'bj' : '北京',
            'sh' : '上海',
            'gz' : '广州',
            'sz' : '深圳',
            'hz' : '杭州',
            'cd' : '成都',
            'cq' : '重庆',
            'wh' : '武汉',
            'xa' : '西安'
        },
        WorkLength = {
            '1' : '1-2',    //0-1年内
            '1_3' : '2-4',  //2-4年
            '3_5' : '4-8',  //5-8年
            '5' : '8-30'    //8年以上
        },
        Constellation = {
            'by' : '白羊座',
            'jn' : '金牛座',
            'szi' : '双子座',
            'jx' : '巨蟹座',
            'sz' : '狮子座',
            'cn' : '处女座',
            'tc' : '天秤座',
            'tx' : '天蝎座',
            'ss' : '射手座',
            'mj' : '摩羯座',
            'sp' : '水瓶座',
            'sy' : '双鱼座'   
        },
        strs = {
            1: {
                sex: {
                    man: '哥们儿',
                    woman: '姐们儿'
                }
            }
        },
        cal = function( setting ){
            return new cal.prototype.init( setting );
        };
    cal.prototype = {
        init : function( setting ){
            this.setting = setting = $.extend( {
                step: 0,
                elements: [],
                prefix: '#JS_sxz_',
                interlude: 'hide',
                defaultPage: '.landing-page',
                data: {
                    degree: null,
                    gender: null,
                    jobType: null,
                    secondClass: null,
                    city: null,
                    workLength: null,
                    scale: null,
                    constellation: null
                },
                ext: {
                    q1: null, //{ ask,ans}
                    q2: null
                }
            } , setting );
            window.__Cal = this;
            this.addHtml();
        },
        addHtml: function(){
            var setting = this.setting,
                step = setting.step,
                prefix = setting.prefix;
            $('.content').remove();
            $('body').append( this.getHtml() );
            this.addEvent();
        },
        getHtml: function(){
            var setting = this.setting,
                step = setting.step,
                data = setting.data,
                sex = data.sex,
                city = data.city,
                jobType = data.jobType,
                degree = data.degree,
                constellation = data.constellation,
                workLength = data.workLength,
                html = '';
            if( step == 0 ){
                html = $('#JS_sxz_0').html();
            };
            if( step == 1 ){
                html = '<div class="content">' +
                            '<h2 class="select-title step-1">日照香炉生紫烟，' + strs[step].sex[sex] + '你在哪混圈？</h2>' +
                            '<div class="city-list clearfix">';
                            for( var i in City ){
                                    html += '<a href="javascript:;" title="" data-city="' + i + '" class="select-btn JS_select_city primary-btn small-btn">' + City[i] + '</a>';
                                };
                            html += '</div>' +
                        '</div>';
                var footHtml = '<div class="footer" id="JS_footer">' +
                                    '<div class="bottom-box">' +
                                        '<div class="earth"><img src="img/common/earth.png" alt="" width="100%"></div>' +
                                        '<div class="person ' + sex + '"><img src="img/rw/' + sex + '/' + sex + '.png" width="100%" alt=""></div>' +
                                    '</div>' +
                                '</div>'; 
                $('body').append( footHtml );
            };
            if( step == 2 ){
                var cityStr = {
                    'bj': '烤鸭文青－羡慕死了，你在帝都。除了吃烤鸭赏话剧，你的看家本领是？',
                    'cd': '天腐之国－羡慕死了，你在成都。除了吃串串逗基友，你的看家本领是？',
                    'gz': '养生胜地－羡慕死了，你在羊城。除了游珠江喝早茶，你的看家本领是？',
                    'hz': '人间天堂—羡慕死了，你在杭州。除了游西湖品龙井，你的看家本领是？',
                    'sh': '红酒小资－羡慕死了，你在魔都。除了品红酒听JAZZ，你的看家本领是？',
                    'sz': '土豪扎堆－羡慕死了，你在深圳。除了吸金狂shopping，你的看家本领是？',
                    'wh': '学霸云集－羡慕死了，你在武汉。除了啃鸭脖赏樱花，你的看家本领是？',
                    'xa': '千年古都－羡慕死了，你在西安，除了逛皇陵忆历史，你的看家本领是？',
                    'cq': '火锅辣妹－羡慕死了，你在山城。除了吃火锅看美女，你的看家本领是？'
                };
                html = '<div class="content">' +
                            '<h2 class="select-title step-1">' + cityStr[city] + '</h2>' +
                            '<div class="job-list clearfix">';
                            for( var i in JobType ){
                                    html += '<a href="javascript:;" title="" ' + ( SecondClass[i] ? 'data-child="true"' : '' ) + ' data-jobType="' + i + '" class="select-btn JS_select_job">' + JobType[i] + '</a>';
                                };
                            html += '</div>' +
                        '</div>';
                var cityFooter = '<div class="bottom-box">' +
                                        '<div class="city ' + city + '"><img src="img/city/' + city + '.png" alt="" width="100%"></div>' +
                                    '</div>';
                $('#JS_footer').prepend( cityFooter );
            };

            if( step == 3 ){
                html = $('#JS_sxz_3').html();
                $('.person').attr( 'class' , 'person ' + sex + ' ' + jobType ).html('<img src="img/rw/' + sex + '/' + jobType + '/' + jobType + '.png" width="100%" alt="">');
            };

            if( step == 4 ){
                html = $('#JS_sxz_4').html();
                $('.city').parent().remove();
                $('.person').html('<img src="img/rw/' + sex + '/' + jobType + '/' + workLength + '/' + jobType + '_' + workLength + '.png" width="100%" alt="">');
                $('#JS_footer').append( $('#JS_footer_decorate').html() );
            };

            if( step == 5 ){
                html = $('#JS_sxz_5').html();
                var degreeHtml = '<div class="degree"><img src="img/degree/' + degree + '.png" alt="" width="100%"></div>';
                $('.person').parent().prepend( degreeHtml );
            };

            if( step == 6 ){
                $('.computer').parent().remove();
                $('.degree').remove();
                $('.degree').remove();
                html = $('#JS_sxz_6').html();
            };

            if( step == 7 ){
                html = $('#JS_sxz_7').html();
                var constelPerson = '<img src="img/rw/' + sex + '/' + jobType + '/' + workLength + '/' + jobType + '_' + workLength + '_' + constellation + '.png" width="100%" alt="">';
                $('.person').html(constelPerson);
            };

            if( step == 8 ){
                html = $('#JS_sxz_8_' + sex).html();
            };
            
            return html;
        },
        addEvent: function(){
            var setting = this.setting,
                step = setting.step;
            if( !setting.elements || !setting.elements[ step ] || !setting.elements[ step ].event || typeof setting.elements[ step ].event != 'function' ) return;
            setting.elements[ step ].event();
        },
        next: function(){
            if( !this.setting.elements.length || !this.setting.elements[ this.setting.step + 1 ] ) return;
            this.setting.step++;
            this.addHtml();
        },
        getSalary: function(){
            var data = this.setting.data,
                ext = this.setting.ext,
                info ={
                    degree: Degree[data.degree],
                    gender: gender[data.sex],
                    jobType: JobType[data.jobType],
                    secondClass: data.secondClass,
                    city: City[data.city],
                    workLength: WorkLength[data.workLength],
                    scale: data.scale,
                    constellation: Constellation[data.constellation],
                    src: $('.person img').attr('src')
                };
            var jsonStr = JSON.stringify({ data: info,ext: ext });

            //console.log(jsonStr)
            // var res ={
            //     current: 10683,
            //     increase: 18,
            //     future: 12636,
            //     min: 8808.100757094368,
            //     summary: "土豪"
            // };
            $.get( '/salary_predict_pro' , {
                p: jsonStr
            },function( res ){
                if( !res ) return;
                $('.content').remove();
                var html = $('#JS_result').html();
                $('body').append( html );
                $('#JS_footer').append('<div class="bottom-box"><div class="coin"><img src="img/common/coin.png" alt="" width="100%"></div></div>');
                $('#JS_current_salary').html( res.current );
                var nextYearHtml = '',
                    nextSalary = parseInt( res.future ).toString();
                for( var i = 0 , l = nextSalary.length ; i < l ; i++ ){
                    nextYearHtml += '<code>' + nextSalary[i] + '</code>';
                };
                $('#JS_next_salary').html(nextYearHtml);
                $('.person').hide();
                $( '#JS_accuracy a' ).on( 'click' , function(){
                    var accuracy = $( this ).attr( 'data-accuracy' );
                    $.get( '/predict_feedback?id=' + res.id + '&accuracy=' + accuracy , {} , function(){});
                    setTimeout( function(){
                        window.location.href = 'more.html' + res.src + '&id=' + res.id;
                    }, 500);
                });
            },'json');
        },
        loadChildClass: function( jobType ){
            var html = '',
                that = this;
            for( var i in SecondClass[jobType] ){
                var secondClass = i;
                html += '<a href="javascript:;" title="" data-secondClass="' + secondClass + '" class="select-btn select_secondClass small-btn"' + ( jobType != 'cp' ? 'data-multi="true"' : '' ) + '>' + SecondClass[jobType][i] + '</a>'
            };
            html += '<br><a href="javascript:;" title="" class="select-btn JS_select_secondClass small-btn confirm-btn">确定</a>';

            $('.job-list').html( html );
            $('.select-title').html('请选择您的职位标签')

            if( jobType == 'gcs' || jobType == 'sj' ){
                $('.job-list,.select-title').addClass('max320');
            };

            $('.select_secondClass').on( 'click' , function(){
                $( this ).toggleClass('active');
                if( !$(this).attr('data-multi') ){
                    $( this ).siblings('.active').removeClass('active');
                };
            });

            $('.JS_select_secondClass').on('click', function(){
                var arr = [],
                    $list = $('.select_secondClass.active');
                if( !$list.length ) return;
                $list.each(function(){
                    var child = SecondClass[ that.setting.data.jobType][$( this ).attr('data-secondClass')];
                    arr.push(child);
                });
                window.__Cal.setting.data.secondClass = arr;
                window.__Cal.next();
            });

        }
    };
    cal.prototype.init.prototype = cal.prototype;

    return function( setting ){
       cal( setting );
    };

})( jQuery );

var getUrlParam = function( param , url ){
    if( !param ) return;
    url = url || location.search.substring(1);
    var arr = url.split('&');
    for ( var i = 0 , l = arr.length ; i < l ; i++ ){
        var arr1 = arr[ i ].split('=');
        if( arr1[0] == param ) return arr1[1];
    };
    return '';
};

/* 加载更多内容页面 */
var loadMore = function(){
    var res = {
            gender: getUrlParam('gender'),
            increase: getUrlParam('increase'),
            src: getUrlParam('src'),
            city: decodeURI( getUrlParam('city') ),
            year: getUrlParam('year'),
            summary: decodeURI( getUrlParam('summary') )
        },
        summarys = {
            '土豪' : 'th',
            '屌丝' : 'ds',
            '小康' : 'xk',
            '温饱' : 'wb'
        },
        sexstr = {
            man: 'nan',
            woman: 'nv'
        },
        comment = function( summary , gender ){
            var txt = {
                'ds': {
                    'man': '岂止拖后腿，简直都拖到脚跟了！',
                    'woman': '岂止拖后腿，简直都拖到脚跟了！'
                },
                'wb': {
                    'man': '跳个槽or求加薪，That is a question !',
                    'woman': '比上不足比下有余，明年待我更努力！'
                },
                'xk': {
                    'man': '不好意思厚，贫富差距又拉大噜！',
                    'woman': '不好意思厚，贫富差距又拉大噜！'
                },
                'th': {
                    'man': '拉高平均水平这种事也不是故意的呢！',
                    'woman': '拉高平均水平这种事也不是故意的呢！'
                }
            };

            return txt[summary][gender];
        },
        headHtml = function( res ){
            var html = '<div class="content">' +
                    '<div class="forecast">' +
                        '<div class="text-center"><img src="img/other/' + ( summarys[res.summary] + sexstr[res.gender] ) + '.png" width="100%" alt=""></div>' +
                        '<div class="text-center house-info">不吃不喝在<cite id="JS_city">' + res.city + '</cite>买房<cite class="arial" id="JS_year">' + res.year + '</cite>年</div>' +
                        '<div class="salary-info text-center">你的薪资涨幅为</div>' +
                        '<h2 class="r-title">' +
                            '<code id="JS_up_percent">' + res.increase + '%</code><br>' +
                            '<span id="JS_comment">' + comment( summarys[res.summary] , res.gender ) + '</span>' +
                        '</h2>' +
                    '</div>' +
                '</div>';
            return html;
        };
    $('body').append( $('#JS_footer_tem').html() );
    if( window.owner ){
        $('#JS_share').find('.text-center').show();
        var system ={
            win : false,
            mac : false,
            xll : false
        };
        //检测平台
        var p = navigator.platform;
        system.win = p.indexOf("Win") == 0;
        system.mac = p.indexOf("Mac") == 0;
        system.x11 = (p == "X11") || (p.indexOf("Linux") == 0);
        //跳转语句
        if( !system.win && !system.mac && !system.xll ){
            $('.jiathis_button_weixin').hide();
        };
    }else{
        $('#JS_play').show();
    };
    var html = headHtml( res ) + $( '#JS_result_' + summarys[res.summary] + sexstr[res.gender] ).html();
    $('#JS_wx_img').after( html );
    $('.person').append( $('<img src="' + res.src + '" width="100%" alt="">') );
};

/* 保留邮箱 */
var loadEmial = function(){
    var html = $('#JS_footer_tem').html(),
        src = getUrlParam('src');
    $('body').prepend( html );
    $('.person').append( $('<img src="' + src + '" width="100%" alt="">') );
};

/* 判断ipad */
function is_iPad(){ 
    var ua = navigator.userAgent.toLowerCase(); 
    if(ua.match(/iPad/i)=="ipad") { 
       return true; 
    } else { 
       return false; 
    } 
}

$(function(){
    var elements = [
        {
            event: function(){
                $( '.JS_choose_sex' ).on( 'click' ,function(){
                    var sex = $( this ).attr('data-sex');
                    window.__Cal.setting.data.sex = sex;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.JS_select_city').on('click',function(){
                    var city = $( this ).attr('data-city');
                    window.__Cal.setting.data.city = city;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.JS_select_job').on('click',function(){
                    var $this = $( this ),
                        jobType = $this.attr('data-jobType');
                    window.__Cal.setting.data.jobType = jobType;
                    if( $this.attr('data-child') ){
                        window.__Cal.loadChildClass( jobType );
                    }else{
                        window.__Cal.next();
                    };
                });
            }
        },
        {
            event: function(){
                $('.JS_select_workLength').on('click',function(){
                    var workLength = $( this ).attr('data-workLength');
                    window.__Cal.setting.data.workLength = workLength;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.JS_select_degree').on('click',function(){
                    var degree = $( this ).attr('data-degree');
                    window.__Cal.setting.data.degree = degree;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.JS_select_scale').on('click',function(){
                    var scale = $( this ).attr('data-scale');
                    window.__Cal.setting.data.scale = scale;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.select_constel').on('click',function(){
                    var constellation = $( this ).attr('data-constel');
                    window.__Cal.setting.data.constellation = constellation;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.JS_select_q1').on('click',function(){
                    var an = $( this ).attr('data-an'),
                        txt = $( this ).text();
                    window.__Cal.setting.ext.q1 = {};
                    window.__Cal.setting.ext.q1[an] = txt;
                    window.__Cal.next();
                });
            }
        },
        {
            event: function(){
                $('.JS_select_q2').on('click',function(){
                    var an = $( this ).attr('data-an'),
                        txt = $( this ).text();
                    window.__Cal.setting.ext.q2 = {};
                    window.__Cal.setting.ext.q2[an] = txt;
                    window.__Cal.getSalary();
                });
            }
        }
    ];
    $('#JS_start_btn').on( 'click' , function(){
        $( this ).closest('.panel').addClass('hide');
        Calculator({
            elements: elements
        });
        $( this ).blur();
    });

    $( document ).on('click', '#JS_restart' , function(){
        $('#JS_footer,.content').remove();
        Calculator({
            elements: elements
        });
        $( this ).blur();
    });

    $(document).on('touchstart', '.select-btn' ,function(){
        $( this ).addClass('hover');
    });

    $(document).on('touchend', '.select-btn' ,function(){
        $( this ).removeClass('hover');
    });

    // $( document ).on( 'click' , '#JS_subscribe' , function(){
    //     window.location.href = 'subscribe.html' + location.search;
    // });

    //大于780像素加载背景
    if( $(window).width() > 780 ){
        $('body').prepend( $('#JS_background').html() );
    };

});
