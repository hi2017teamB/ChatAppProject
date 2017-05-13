function redirect_user_mag(){
  obj = document.test.user;

  index = obj.selectedIndex;
  href = obj.options[index].value;
  location.href = href;
}