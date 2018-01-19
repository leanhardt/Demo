$(function () {
   $("#captcha-btn").click(function (event) {
       event.preventDefault();
       var email = $("input[name='email']").val();
       if(!email){
           fdalert.alertInfoToast("请输入邮箱！");
           return;
       }else{
            Flask_Demo.get({
               'url':'/cms/email_captcha/',
               'data':{
                   'email':email
               } ,
                'success':function (data) {
                    if(data['code'] == 200){
                        fdalert.alertSuccessToast("邮件发送成功！注意查收！");
                    }else{
                        fdalert.alertInfo(data['message']);
                    }
                },
                'fail':function (error) {
                    fdalert.alertNetworkError();
                }
            });
       }
   });
});

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();
        console.log(email);
        console.log(captcha);
        Flask_Demo.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha':captcha
            },
            'success':function (data) {
                if(data['code'] == 200){
                    fdalert.alertSuccessToast("邮箱修改成功！");
                    emailE.val("");
                    captchaE.val("");
                }else{
                    fdalert.alertInfo(data['message']);
                }
            },
            'fail':function (error) {
                fdalert.alertNetworkError();
            }
        })
    })
});