// 创建文件悬浮窗-打开-start
function openCreateCodeFile() {
    document.getElementById('windowLight').style.display = 'block';
    document.getElementById('windowFade').style.display = 'block';
    // console.log(document.body.scrollHeight);
    fadeDiv = document.getElementsByName("windowFade")[0];
    fadeDiv.style.height = document.body.scrollHeight + "px";
    // targetHeight = Number(document.getElementsByClassName("header_section")[0].style.height)
    // // + Number(document.getElementsByClassName("file_section layout_padding")[0].style.height) + Number(document.getElementsByClassName(" info_section layout_padding2")[0].style.height)
    // console.log(document.getElementsByClassName("header_section")[0].style)
    // fadeDiv.style.height = targetHeight + "px"
}
// 创建文件悬浮窗-打开-end


// 创建文件悬浮窗-创建-start
$("[name='window_create_Button']").click(function () {
    var fileName = document.getElementsByName('window_name_input')[0].value;
    if (fileName === "") {
        $.confirm({
            title: '错误',
            content: '文件名不能为空',
            buttons: {
                ok: {
                    text: '确认',
                    btnClass: 'btn-primary',
                },
            }
        });
        return;
    }
    else {
        $.ajax({
            url: "/create_code_file_port/",
            type: "post",
            dataType: "json",
            data: {
                fileName: fileName,
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            success: function (result) {
                if (result.returnCode == 'true') {
                    // 生成html-start
                    var boxDiv = document.createElement("div");//外层div-1
                    boxDiv.classList.add("box");
                    boxDiv.setAttribute("name", "box_" + result.id);
                    var urlDiv = document.createElement("div");//隐藏链接div用于分享-2
                    urlDiv.setAttribute("hidden", "true");
                    urlDiv.setAttribute("name", "share_url");
                    urlDiv.innerText = "http://127.0.0.1:8000/editor/" + result.id;
                    boxDiv.appendChild(urlDiv)
                    var div2 = document.createElement("div");//外层div-2
                    div2.setAttribute("style", "display: inline-block;width: 90%;");
                    boxDiv.appendChild(div2)
                    var elem_a = document.createElement("a");//a标签-2
                    elem_a.setAttribute("href", "");
                    elem_a.setAttribute("style", "color: #000000;width: 100%;");
                    div2.appendChild(elem_a);
                    var detail_div = document.createElement("div");//div-3
                    detail_div.classList.add("detail-box");
                    detail_div.setAttribute("type", result.id);
                    detail_div.setAttribute("name", "file_id_" + result.id);
                    elem_a.appendChild(detail_div);
                    var elem_h4 = document.createElement("h4");//文件名-4-1
                    elem_h4.innerHTML = document.getElementsByName('window_name_input')[0].value;
                    detail_div.appendChild(elem_h4);
                    var elem_p = document.createElement("p");//信息-4-2
                    elem_p.setAttribute("style", "font-size:15px")
                    elem_p.innerHTML = "创建人:" + result.userName + "&nbsp&nbsp&nbsp&nbsp&nbsp" + "创建时间:" + result.createTime + "&nbsp&nbsp&nbsp&nbsp&nbsp" + "修改时间:" + result.changeTime
                    detail_div.appendChild(elem_p);
                    //按钮-start
                    var div2_1 = document.createElement("div");//外层div-2
                    div2_1.setAttribute("style", "display: inline-block;width: 5%;");
                    boxDiv.appendChild(div2_1)
                    var div3 = document.createElement("div");//外层div-3
                    div3.classList.add("dropdown");
                    div3.setAttribute("style", "display: inline-block;width: 100%;");
                    div2_1.appendChild(div3)
                    var button1 = document.createElement("button");//button-3
                    button1.setAttribute("type", "button")
                    button1.classList.add("btn", "dropdown-toggle")
                    button1.setAttribute("id", "dropdownBtn")
                    button1.setAttribute("data-toggle", "dropdown")
                    button1.setAttribute("style", "font-weight:bolder;font-size: 30px;border: 0px;")
                    button1.innerText = "···"
                    div3.appendChild(button1)
                    var ul1 = document.createElement("ul");//ul-4
                    ul1.classList.add("dropdown-menu")
                    ul1.setAttribute("id", "dropdownMenu")
                    ul1.setAttribute("role", "menu")
                    ul1.setAttribute("aria-labelledby", "dropdownMenu1")
                    div3.appendChild(ul1)
                    var li1 = document.createElement("li");//li-5-1
                    li1.setAttribute("role", "presentation")
                    li1.setAttribute("id", "menu_item")
                    li1.setAttribute("style", "margin-bottom: 5px;margin-top: 5px;")
                    ul1.appendChild(li1)
                    var li_a1 = document.createElement("a");//li-6-1
                    li_a1.setAttribute("role", "menuitem")
                    li_a1.setAttribute("tabindex", "-1")
                    li_a1.setAttribute("href", "javascript:void(0);")
                    li_a1.setAttribute("id", "menu_a")
                    li_a1.setAttribute("onclick", "download_code(" + result.id + ")")
                    li_a1.innerText = "导出"
                    li1.appendChild(li_a1)
                    var li2 = document.createElement("li");//li-5-2
                    li2.setAttribute("role", "presentation")
                    li2.setAttribute("id", "menu_item")
                    li2.setAttribute("style", "margin-bottom: 5px;margin-top: 5px;")
                    ul1.appendChild(li2)
                    var li_a2 = document.createElement("a");//li-6-2
                    li_a2.setAttribute("role", "menuitem")
                    li_a2.setAttribute("tabindex", "-1")
                    li_a2.setAttribute("href", "javascript:void(0);")
                    li_a2.setAttribute("id", "menu_a")
                    li_a2.setAttribute("onclick", "rename_code(" + result.id + ")")
                    li_a2.innerText = "重命名"
                    li2.appendChild(li_a2)
                    var li3 = document.createElement("li");//li-5-3
                    li3.setAttribute("role", "presentation")
                    li3.setAttribute("id", "menu_item")
                    li3.setAttribute("style", "margin-bottom: 5px;margin-top: 5px;")
                    ul1.appendChild(li3)
                    var li_a3 = document.createElement("a");//li-6-3
                    li_a3.setAttribute("role", "menuitem")
                    li_a3.setAttribute("tabindex", "-1")
                    li_a3.setAttribute("href", "javascript:void(0);")
                    li_a3.setAttribute("id", "menu_a")
                    li_a3.setAttribute("name", "share_code")
                    li_a3.setAttribute("onclick", "share_code(" + result.id + ")")
                    li_a3.innerText = "分享"
                    li3.appendChild(li_a3)
                    var li4 = document.createElement("li");//li-5-4
                    li4.setAttribute("role", "presentation")
                    li4.setAttribute("id", "menu_item")
                    li4.setAttribute("style", "margin-bottom: 5px;margin-top: 5px;")
                    ul1.appendChild(li4)
                    var li_a4 = document.createElement("a");//li-6-3
                    li_a4.setAttribute("role", "menuitem")
                    li_a4.setAttribute("tabindex", "-1")
                    li_a4.setAttribute("href", "javascript:void(0);")
                    li_a4.setAttribute("id", "menu_a")
                    li_a4.setAttribute("onclick", "delete_code(" + result.id + ")")
                    li_a4.setAttribute("style", "color:#ff4343")
                    li_a4.innerText = "删除"
                    li4.appendChild(li_a4)
                    //按钮-end
                    var firstChildNode = document.getElementsByName('codeFileList')[0].firstChild;//获取父元素的第一个子元素，用于插入
                    document.getElementsByName('codeFileList')[0].insertBefore(boxDiv, firstChildNode);
                    // 生成html-end
                    document.getElementsByName('window_name_input')[0].value = '';//清空内容
                    document.getElementById('windowLight').style.display = 'none';
                    document.getElementById('windowFade').style.display = 'none'
                }
                if (result.returnCode == 'false') {
                    $.confirm({
                        title: '错误',
                        content: "发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")",
                        buttons: {
                            ok: {
                                text: '确认',
                                btnClass: 'btn-primary',
                            },
                        }
                    });
                }
            }
        })
    }
});
// 创建文件悬浮窗-创建-end


// 创建文件悬浮窗-取消-start
$("[name='window_cancel_Button']").click(function () {
    document.getElementsByName('window_name_input')[0].value = '';//清空内容
    document.getElementById('windowLight').style.display = 'none';
    document.getElementById('windowFade').style.display = 'none';

});
// 创建文件悬浮窗-取消-end


// 文件-下载-start
function download_code(file_id) {
    // var fileId = document.getElementsByName('file_id')[0].getAttribute("type");
    window.location.href = "/download_port/" + file_id;
}
// 文件-下载-end


renameFileId = ''
// 文件-重命名-start
function rename_code(file_id) {
    document.getElementById('windowLight_rename').style.display = 'block';
    document.getElementById('windowFade_rename').style.display = 'block'
    document.getElementsByName('window_rename_input')[0].setAttribute('placeholder', document.getElementsByName('file_id_' + file_id)[0].children[0].innerText);//清空内容
    renameFileId = file_id
}
// 文件-重命名-end
// 重命名-start
$("[name='window_rename_Button']").click(function () {
    $.ajax({
        url: "/rename_port/",
        type: "post",
        dataType: "json",
        data: {
            newName: document.getElementsByName("window_rename_input")[0].value,
            fileId: renameFileId,
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (result) {
            if (result.returnCode == 'true') {
                document.getElementsByName('file_id_' + renameFileId)[0].children[0].innerText = document.getElementsByName("window_rename_input")[0].value;
                document.getElementsByName('window_rename_input')[0].value = '';//清空内容
                document.getElementById('windowLight_rename').style.display = 'none';
                document.getElementById('windowFade_rename').style.display = 'none';
            }
            if (result.returnCode == 'false') {
                $.confirm({
                    title: '错误',
                    content: "发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")",
                    buttons: {
                        ok: {
                            text: '确认',
                            btnClass: 'btn-primary',
                        },
                    }
                });
            }
        }
    })
})
// 重命名-end
$("[name='window_rename_cancel_Button']").click(function () {
    document.getElementsByName('window_rename_input')[0].value = '';//清空内容
    document.getElementById('windowLight_rename').style.display = 'none';
    document.getElementById('windowFade_rename').style.display = 'none';
});
// 重命名悬浮窗-取消-end



// 文件-分享-start
function share_code(file_id) {
    var content = $("[name='share_url']").html();
    var clipboard = new Clipboard("[name='share_code']", {
        text: function () {
            return content;
        }
    });
    clipboard.on('success', function (e) {
        $.confirm({
            title: '分享成功',
            content: '分享链接已经复制到您的剪贴板，快去分享吧',
            buttons: {
                ok: {
                    text: '确认',
                    btnClass: 'btn-primary',
                },
            }
        });
    });

    clipboard.on('error', function (e) {
        console.log(e);
    });
}
// 文件-分享-end


// 文件-删除-start
function delete_code(file_id) {
    $.confirm({
        title: '警告',
        content: '确认删除' + document.getElementsByName('file_id_' + file_id)[0].children[0].innerText + '？',
        buttons: {
            ok: {
                text: '确认删除',
                textColor: '#000000',
                action: function () {
                    $.ajax({
                        url: "/delete_port/",
                        type: "post",
                        dataType: "json",
                        data: {
                            fileId: file_id,
                            csrfmiddlewaretoken: '{{ csrf_token }}',
                        },
                        success: function (result) {
                            if (result.returnCode == 'true') {
                                boxDiv = document.getElementsByName("box_" + file_id)[0]
                                boxDiv.remove();
                            }
                            if (result.returnCode == 'false') {
                                $.confirm({
                                    title: '错误',
                                    content: "发生错误请稍后重试===>" + result.returnCode + "(" + result.returnContent + ")",
                                    buttons: {
                                        ok: {
                                            text: '确认',
                                            btnClass: 'btn-primary',
                                        },
                                    }
                                });
                            }
                        }
                    })
                }
            },
            cancel: {
                text: '取消',
                btnClass: 'btn-primary'
            }
        }
    });
}
// 文件-删除-end
