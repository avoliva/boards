var llmlSpoiler, quickpost, quickpost_quote;

quickpost = function() {
  $("#pageexpander").toggle();
  $("#quickpost").toggle();
  $("#open").toggle();
  $("#close").toggle();
  if ($("#pageexpander").is(":visible")) {
    return $("#message").focus();
  }
};

quickpost_quote = function(message_id) {
  var id, quote_data, req;
  if (!$("#pageexpander").is(":visible")) {
    quickpost();
  }
  quote_data = message_id.split(",");
  id = quote_data[2].split("@");
  req = "id=" + id[0] + "&topic=" + quote_data[1] + "&r=" + id[1] + "&output=json";
  if (quote_data[0] === "l") {
    req += "&link=1";
  }
  $.ajax({
    url: "/mcreate/",
    dataType: "json",
    data: req,
    success: function(result) {
      var message_body, message_split, sig;
      message_body = $("#qpmessage").val();
      message_split = $("#qpmessage").val().split("---");
      message_body = message_split[0];
      sig = message_split[message_split.length - 1];
      return $("#qpmessage").val(message_body + "<quote msgid=\"" + quote_data[0] + "," + quote_data[1] + "," + quote_data[2] + "\">" + result["message"] + "</quote>\n" + "---" + sig);
    }
  });
  return false;
};

llmlSpoiler = function(id) {
  return $(id).click(function() {
    $(id).toggleClass("spoiler_opened", "spoiler_closed");
    $(id).toggleClass("spoiler_closed", "spoiler_opened");
    $("img").lazyload();
    return false;
  });
};

$(function() {
  $("img").lazyload();
  return $("#qptoggle").click(function() {
    quickpost();
    return false;
  });
});

$(window).keypress(function(a) {
  if (a.charCode === 96) {
    if (!$("#qpmessage").is(":focus")) {
      $("#qptoggle").click();
      a.preventDefault();
      $("#qpmessage").focus();
    }
  }
  return a;
});
