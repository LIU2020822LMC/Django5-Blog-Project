$(function () {
  function bindCaptchaBtnClick() {
    // 获取 CSRF 令牌
    function getCSRFToken() {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, 10) === "csrftoken=") {
            cookieValue = decodeURIComponent(cookie.substring(10));
            break;
          }
        }
      }
      return cookieValue;
    }

    $("#captcha-btn").click(function (event) {
      let $this = $(this);
      let email = $("input[name = 'email']").val();
      if (!email) {
        alert("请输入邮箱！");
        return;
      }
      //取消按钮的点击事件
      $this.off("click");

      //发送ajax请求
      $.ajax("/auth/captcha?email=" + email, {
        method: "GET",
        headers: {
          "X-CSRFToken": getCSRFToken(), // 使用您已有的getCSRFToken函数
        },
        success: function (result) {
          if (result["code"] == 200) {
            alert("验证码发送成功！");
          } else {
            alert(result["message"]);
          }
        },
        fail: function (error) {
          console.log(error);
        },
      });

      //倒计时
      let countdown = 6;
      let timer = setInterval(function () {
        if (countdown <= 0) {
          $this.text("获取验证码");
          //清掉定时器
          clearInterval(timer);
          //重新绑定事件
          bindCaptchaBtnClick();
        } else {
          countdown--;
          $this.text(countdown + "s");
        }
      }, 1000);
    });
  }
  bindCaptchaBtnClick();
});
