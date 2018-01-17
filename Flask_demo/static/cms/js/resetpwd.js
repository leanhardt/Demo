$(function () {
    $("#submit").click(function (event) {
        //evemt.prevemtDefault
        //是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwe]");
        var newpwdE = $("input[name=newpwe]");
        var newpwdE2 = $("input[name=newpwe2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwdE2.val();

        Flask_Demo.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'succes': function (data) {
                console.log(data)
            },
            'fail': function (error) {
                console.log(error)
                
            }
        })
    })
})