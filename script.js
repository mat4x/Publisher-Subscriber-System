function publish() {
	var message   = document.getElementById("message_box").value.trim()
	var user_name = document.getElementById("pub_usr_name").value.trim()

	console.log(message)
	if (user_name == ""){
		alert("Please enter user name")
		return 0; }

	if (message == ""){
		alert("Please write some content");
		return 0; }

	$.post("", {"action":"publish", "publisher":user_name, "content":message})
	alert("Article has been Published");
}

