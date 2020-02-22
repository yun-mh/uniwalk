(function() {
  // pusherのAPI設定
  var pusher = new Pusher("768af5bb1417be83adc3", {
    authEndpoint: "/chats/pusher/auth/",
    cluster: "ap3",
    encrypted: true
  });

  // チャットのデフォルト設定
  let chat = {
    email: undefined,
    myChannel: undefined
  };

  // DOMの取得
  const chatPage = $(document);
  const chatBtn = $(".chatbubble");
  const chatCloseBtn = $(".closeBtn");
  const chatWindow = $(".chat-window");
  const chatBody = $(".chat-window");

  // UIを操作する関数の定義
  let helpers = {
    // チャットウィンドウの操作
    ToggleChatWindow: function() {
      chatBtn.toggleClass("hidden");
      chatWindow.toggleClass("hidden");
    },

    // チャットルームかログインかを判断し、適切な内容を表示
    ShowAppropriateChatDisplay: function() {
      chat.email
        ? helpers.ShowChatRoomDisplay()
        : helpers.ShowChatInitiationDisplay();
    },

    // チャットする前に認証する画面を表示
    ShowChatInitiationDisplay: function() {
      chatBody.find(".chats").addClass("hidden");
      chatBody.find(".login-screen").removeClass("hidden");
    },

    // チャットルームを表示
    ShowChatRoomDisplay: function() {
      chatBody.find(".chats").removeClass("hidden");
      chatBody.find(".login-screen").addClass("hidden");

      setTimeout(function() {
        chatBody.find(".loader-wrapper").hide();
        chatBody.find(".input, .msgs").toggleClass("hidden");
      }, 2000);
    },

    // チャットウィンドウにメッセージを入れる
    NewChatMessage: function(message) {
      if (message !== undefined) {
        const messageClass = message.sender !== chat.email ? "support" : "user";
        const senderInfo =
          message.sender !== chat.email ? "Support" : message.email;

        chatBody.find("ul.msgs").append(
          `<li class="${messageClass} rounded">
              <div class="${messageClass}">${senderInfo}</div>
              <div>${message.text}</div>
          </li>`
        );
        $(".msgs").scrollTop($(".msgs")[0].scrollHeight);
      }
    },

    // 管理者にメッセージを送る
    SendMessageToSupport: function(evt) {
      evt.preventDefault();

      let createdAt = new Date();
      createdAt = createdAt.toLocaleString();

      const message = $("#newMessage")
        .val()
        .trim();

      chat.myChannel.trigger("client-guest-new-message", {
        sender: chat.email,
        email: chat.email,
        text: message,
        createdAt: createdAt
      });

      helpers.NewChatMessage({
        text: message,
        email: chat.email,
        sender: chat.email
      });

      console.log("Message added!");

      $("#newMessage").val("");
    },

    // チャットセッションにアクセスする
    LogIntoChatSession: function(evt) {
      const email = $("#email")
        .val()
        .trim()
        .toLowerCase();

      chatBody
        .find("#loginScreenForm input, #loginScreenForm button")
        .attr("disabled", true);

      if (email !== "" && email.length >= 5) {
        axios.post("/chats/guest/", { email }).then(response => {
          chat.email = email;
          chat.myChannel = pusher.subscribe("private-" + response.data.email);
          helpers.ShowAppropriateChatDisplay();
        });
      } else {
        alert("Enter a valid name and email.");
      }

      evt.preventDefault();
    }
  };

  // 管理者からのメッセージを受信する
  pusher.bind("client-support-new-message", function(data) {
    helpers.NewChatMessage(data);
  });

  // イベントリスナーの定義
  chatPage.ready(helpers.ShowAppropriateChatDisplay);
  chatBtn.on("click", helpers.ToggleChatWindow);
  chatCloseBtn.on("click", helpers.ToggleChatWindow);
  $("#loginScreenForm").on("submit", helpers.LogIntoChatSession);
  $("#messageSupport").on("submit", helpers.SendMessageToSupport);
})();
