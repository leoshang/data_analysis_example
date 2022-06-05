http://m.titan007.com/script/letgoalOverunderData.js

var GoalCn2 = ["0", "0/0.5", "0.5", "0.5/1", "1", "1/1.5", "1.5", "1.5/2", "2", "2/2.5", "2.5", "2.5/3", "3", "3/3.5", "3.5", "3.5/4", "4", "4/4.5", "4.5", "4.5/5", "5", "5/5.5", "5.5", "5.5/6", "6", "6/6.5", "6.5", "6.5/7", "7", "7/7.5", "7.5", "7.5/8", "8", "8/8.5", "8.5", "8.5/9", "9", "9/9.5", "9.5", "9.5/10", "10", "10/10.5", "10.5", "10.5/11", "11", "11/11.5", "11.5", "11.5/12", "12", "12/12.5", "12.5", "12.5/13", "13", "13/13.5", "13.5", "13.5/14", "14"];
function LoadData() {
    var url = "/HandicapDataInterface.ashx?scheid=" + scheduleId + "&type=1&oddskind=" + oddskind + "&isHalf=" + isHalf;
    bomHelper.ajaxGet(url, function (data) {
        maketable(data);
    });
} 
//生成公司列表及对应最后一条即时盘数据
function maketable(data) {
    var obj;
    var html = new Array();
    var companysHtml = new Array();
    if(data!="")
        obj = JSON.parse(data);

    if (obj.companies != undefined && obj.companies.length > 0) {
        for (var i = 0; i < obj.companies.length; i++) {
            var d = obj.companies[i];
            for (var j = 0; j < d.details.length; j++) {
                if (j == 0) {
                    var muti = "";
                    if (d.details.length > 1) {
                        muti = '<span id="mainFlg_' + d.companyId + '" class="showMore" onclick="showMultiData(' + d.companyId + ')"></span>';
                    }
                    companysHtml.push('<div id="main_' + d.companyId + '" class="CBtn">' + muti + '<span onclick="ShowMainOddsDetail(' + oddskind + ',' + d.companyId + ',' + date("YmdHis", obj.matchTime) + ')"' + (d.details.length > 1 ? "" : " class='singleBtn' ") + '>' + d.nameCn + '</span></div>');
                } else {
                    companysHtml.push('<div onclick = "ShowOddsDetail(' + oddskind + ',' + d.details[j].oddsId + ',this)" data-cId="' + d.companyId + '" style="display:none;" class="pang">盘(' + d.details[j].num + ')</div>');
                }
                var cid = j != 0 ? " data-cId ='" + d.companyId + "' style='display:none;'" : "";
                var onclickFunction = j == 0 ? "ShowMainOddsDetail(" + oddskind + "," + d.companyId + "," + date("YmdHis", obj.matchTime) + ")" : "ShowOddsDetail(" + oddskind + "," + d.details[j].oddsId + ",this)";
                html.push('<div onclick ="' + onclickFunction + '"' + cid + '>');
                html.push('<div class="oddsdata"><span>' + returnFloat(d.details[j].firstHomeOdds) + '</span>' + '<span>' + (d.details[j].firstDrawOdds == undefined ? 0 : Goal2GoalCn(d.details[j].firstDrawOdds)) + '</span>' + '<span>' + returnFloat(d.details[j].firstAwayOdds) + '</span></div>');
                html.push('<div class="oddsdata"><span ' + SetClass(d.details[j].homeOdds, d.details[j].firstHomeOdds) + '>' + returnFloat(d.details[j].homeOdds) + '</span>' + '<span ' + SetClass(d.details[j].drawOdds, d.details[j].firstDrawOdds) + '>' + (d.details[j].drawOdds == undefined ? 0 : Goal2GoalCn(d.details[j].drawOdds)) + '</span>' + '<span ' + SetClass(d.details[j].awayOdds, d.details[j].firstAwayOdds) + '>' + returnFloat(d.details[j].awayOdds) + '</span></div>');
                html.push('</div>');
            }
        }
        document.getElementById("oddsData").innerHTML = html.join("");
        document.getElementById("oddsCompany").innerHTML = companysHtml.join("");
    }
}
//显示多盘口详细页
function ShowOddsDetail(oddskind, oddsid, even) {
    var url = "/HandicapDataInterface.ashx?scheid=" + scheduleId + "&type=2&oddskind=" + oddskind + "&oddsid=" + oddsid + "&isHalf=" + isHalf;
    bomHelper.ajaxGet(url, function (data) {
        makeDetailTable(data, false);
        changeSelectCompany();
        document.getElementById("oddsData").style.display = "none";
        even.className = "pang on";
        document.getElementById("content").className = "Live";
        document.getElementById("oddsTitle").className = "OddTH Live";
        document.getElementById("footer").style.display = "none";
        if (document.getElementById("RealData") != null)
            document.getElementById("RealData").style.paddingBottom = (document.getElementById("mainHead").offsetHeight + document.getElementById("oddsTitle").offsetHeight) + "px";
    });
}
//var lastOddsKind = "", lastCompanyId = "", lastMatchtime = "";
//显示主盘详细页
function ShowMainOddsDetail(oddskind, companyid,matchtime) {

    var url = "/HandicapDataInterface.ashx?scheid=" + scheduleId + "&type=3&oddskind=" + oddskind + "&companyid=" + companyid + "&matchtime=" + matchtime + "&isHalf=" + isHalf;
    //lastOddsKind = oddskind;
    //lastCompanyId = companyid;
    //lastMatchtime = matchtime;
    bomHelper.ajaxGet(url, function (data) {
        makeDetailTable(data, true);
        changeSelectCompany();
        document.getElementById("oddsData").style.display = "none";
        document.getElementById("main_" + companyid).className = "CBtn on";
        document.getElementById("footer").style.display = "none";
        document.getElementById("RealData").style.paddingBottom = (document.getElementById("mainHead").offsetHeight + document.getElementById("oddsTitle").offsetHeight) + "px";
    });
}
function makeDetailTable(data,isMainOdds) {
    var obj;
    var html = new Array();
    if (data != "")
        obj = JSON.parse(data);
    if (isMainOdds) {
        GetOddsDetail(obj, 1, isMainOdds);
    } else {
        GetOddsDetail(obj.details, 1, isMainOdds);
    }
}
//显示隐藏多盘口公司列表
function showMultiData(id) {
    $("[data-cid=" + id + "]").each(function () {
        if ($(this).css('display') == 'none') {
            $(this).show();
        }
        else {
            $(this).hide();
        }
    });
    var arr = document.getElementById("mainFlg_" + id);
    if (arr.className == "showMore") {
        arr.className = "showMore on";
    } else {
        arr.className = "showMore";
    }
}
//生成盘口详细页
function GetOddsDetail(data, odType, isMainOdds) {
    //var defaultHtml = "<div class='OddTH'><span>详细变化</span><span class='closeBtn' onclick='closeOddsDetail()'></span></div>";
    if (data != undefined && data != "") {
        var arrHtml = new Array();
        var runningHtml = new Array();
        var goalColor = "#ffe076";
        arrHtml.push('<ul id="RealData" class="oddsDetail">');
        for (var i = 0; i < data.length; i++) {
            if (isMainOdds) {
                var od = new OddsDetail(data[i]);
            }
            else {
                var od = new MultiOddsDetail(data[i]);
            }
            if (i == data.length - 1) {
                arrHtml.push('<li><div>' + od.Score + '</div><div>' + od.HomeOdds + '</div><div>' + (odType == 4 ? od.PanKou : Goal2GoalCn(od.PanKou)) + '</div><div>' + od.AwayOdds + '</div><div>' + od.ModifyTime + '</div></li>');
                break;
            }
            if (isMainOdds) {
                var earlyOd = new OddsDetail(data[i + 1]);
            }
            else {
                var earlyOd = new MultiOddsDetail(data[i + 1]);
            }
            if (od.isRunning) {
                runningHtml.push(CreateTr(od, earlyOd, i, odType));
            }
            else {
                arrHtml.push(CreateTr(od, earlyOd, i, odType));
            }
        }

        arrHtml.push('</ul>');
        if (runningHtml.length > 0) {
            //runningHtml.unshift('<div class="subTool" onclick="showRunningData()"><span class="state red">滚</span><span id="runningText">点击展开滚球指数</span><i id="runningFlg" class="down"></i></div><ul class="oddsDetail" id="runningData" style="display:none;">');
            runningHtml.unshift('<ul class="oddsDetail" id="runningData" style="display:none;">');
            runningHtml.push('</ul>');
            document.getElementById("content").className = "Running";
            document.getElementById("oddsTitle").className = "OddTH Running";
        }
        else {
            document.getElementById("content").className = "Live";
            document.getElementById("oddsTitle").className = "OddTH Live";
        }

        document.getElementById("oddsDetail").innerHTML = runningHtml.join("") + arrHtml.join("");
        document.getElementById("oddsDetail").style.display = "";
    }
    else {
        document.getElementById("oddsDetail").innerHTML = "<div id='noData' style='text-align:center;'>暂无数据</div>";
        document.getElementById("oddsDetail").style.display = "";
    }

}

function CreateTr(od, earlyOd, i, odType) {
    var tr = "<li>";
    if (od.Score != earlyOd.Score && earlyOd.HappenTime != "") {
        tr = "<li class='bgcolor'>"
    }
    if (earlyOd.isClosed) {
        if (od.isClosed) {
            tr += '<div>' + od.Score + '</div><div colspan="3">封</div><div>' + od.ModifyTime + '</div></li>';
        } else {
            tr += "<div>" + od.Score + "</div><div>" + od.HomeOdds + "</div><div>" + (odType == 4 ? od.PanKou : Goal2GoalCn(od.PanKou)) + "</div><div>" + od.AwayOdds + "</div><div>" + od.ModifyTime + "</div></li>";
        }
    }
    else {
        if (od.isClosed) {
            tr += '<div>' + od.Score + '</div><div colspan="3">封</div><div>' + od.ModifyTime + '</td></li>';
        }
        else {
            tr += "<div>" + od.Score + "</div>";
            tr += "<div " + SetClass(od.HomeOdds, earlyOd.HomeOdds) + ">" + od.HomeOdds + "</div>";
            tr += "<div " + SetClass(od.PanKou, earlyOd.PanKou) + ">" + (odType == 4 ? od.PanKou : Goal2GoalCn(od.PanKou)) + "</div>";
            tr += "<div " + SetClass(od.AwayOdds, earlyOd.AwayOdds) + ">" + od.AwayOdds + "</div>";
            tr += "<div>" + od.ModifyTime + "</div>";
            tr += "</li>";
        }
    }
    return tr;
}
function SetClass(od, earlyod) {
    if (od == earlyod) {
        return "";
    }
    else {
        if (od > earlyod) {
            return "class='red'";
        } else {
            return "class='green'";
        }
    }
}
function Goal2GoalCn(goal) {
    if (goal == null || goal + "" == "")
        return "";
    else {
        if (goal > 10 || goal < -10) return goal + "";
        if (goal >= 0) return GoalCn2[parseInt(goal * 4)];
        else return "-" + GoalCn2[Math.abs(parseInt(goal * 4))];
    }
}
function OddsDetail(data) {
    this.AwayOdds = returnFloat(data.AwayOdds);
    this.HappenTime = data.HappenTime;
    this.HomeOdds = returnFloat(data.HomeOdds);
    this.isClosed = (data.IsClosed == "封");
    this.PanKou = data.PanKou;
    this.Score = data.Score;
    this.isRunning = false;
    if (data.Score == "初" || data.Score == "即" || data.Score == "早") {
        this.ModifyTime = data.ModifyTime.substring(4, 6) + "-" + data.ModifyTime.substring(6, 8) + " " + data.ModifyTime.substring(8, 10) + ":" + data.ModifyTime.substring(10, 12);
    } else {
        this.ModifyTime = this.HappenTime == "中场" || this.HappenTime == "半" ? this.HappenTime : this.HappenTime + "'";
        this.isRunning = true;
    }
}
function MultiOddsDetail(data) {
    this.AwayOdds = returnFloat(data.awayOdds);
    this.HappenTime = "";
    this.HomeOdds = returnFloat(data.homeOdds);
    this.isClosed = false;
    this.PanKou = data.drawOdds == undefined ? "0" : data.drawOdds;
    this.Score = data.kind == "REAL" ? "即" : "早";
    this.isRunning = false;
    this.ModifyTime = date('m-dTh:i',data.modifyTime);
}
function showRunningData() {
    var obj = document.getElementById("runningData");
    if (obj.style.display == "none") {
        obj.style.display = "";
    } else {
        obj.style.display = "none";
    }
    obj = document.getElementById("runningFlg");
    obj.className = obj.className == "up" ? "down" : "up";
    document.getElementById("runningText").innerText = obj.className == "up" ? "点击收起滚球数据" : "点击展开滚球数据";
    var objRealData = document.getElementById("RealData");
    objRealData.style.paddingTop = obj.className == "up" ? "0px" : "26px";

}
function closeOddsDetail() {
    document.getElementById("oddsDetail").style.display = "none";
    document.getElementById("oddsData").style.display = "";
    document.getElementById("content").className = "Default";
    document.getElementById("oddsTitle").className = "OddTH Default";
    changeSelectCompany();
    document.getElementById("footer").style.display = "";
}
function changeSelectCompany() {
    $("[data-cId]").each(function () {
        if ($(this).hasClass("on")) {
            $(this).removeClass("on");
        }
    });
    $("div[class='CBtn on']").each(function () {
        var obj = $(this);
        $(this).removeClass("on");
    });
}
function HalfChange(obj) {
    isHalf = obj.options[obj.selectedIndex].value;
    LoadData();
    document.getElementById("oddsDetail").style.display = "none";
    document.getElementById("oddsData").style.display = "";
    document.getElementById("content").className = "Default";
    document.getElementById("oddsTitle").className = "OddTH Default";
    document.getElementById("footer").style.display = "";
}
function returnFloat(value) {
    var value = Math.round(parseFloat(value) * 100) / 100;
    var xsd = value.toString().split(".");
    if (xsd.length == 1) {
        value = value.toString() + ".00";
        return value;
    }
    if (xsd.length > 1) {
        if (xsd[1].length < 2) {
            value = value.toString() + "0";
        }
        return value;
    }
}
