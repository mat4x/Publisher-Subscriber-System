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

function subscribe(channel_usr_name){
	var user_name = document.getElementById("sub_usr_name").innerHTML;
	console.log(user_name, channel_usr_name)

	$.post("", {"action":"subscribe", "sub":user_name, "channel":channel_usr_name})
	document.getElementById(channel_usr_name+"_btn").style.background = "grey";
	document.getElementById(channel_usr_name+"_btn").innerHTML = "Subscribed";

}

function login_sub(){
	var user_name = localStorage.getItem("sub_usr_name");

	if (user_name == null || user_name == "null"){
		subscriber_user_name = prompt("Enter Username: ");
		localStorage.setItem("sub_usr_name",subscriber_user_name);
	}
	else{
		subscriber_user_name = user_name; }
	$.post("", {"action":"sub_login", "subscriber":subscriber_user_name})
}

function set_sub_usr_name(){
	document.getElementById("sub_usr_name").innerHTML = localStorage.getItem("sub_usr_name");
}