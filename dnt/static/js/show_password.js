function show_pass() {
    var x = document.getElementById("id_password1");

    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }

    var y = document.getElementById("id_password2");

    if (y.type === "password") {
      y.type = "text";
    } else {
      y.type = "password";
    }
    
  }