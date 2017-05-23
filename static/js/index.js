function redirect_user_mag(){
  obj = document.test.user;

  index = obj.selectedIndex;
  href = obj.options[index].value;
  location.href = href;
}

function redirect_group_mag(){
  obj = document.group.group;

  index = obj.selectedIndex;
  href = obj.options[index].value;
  location.href = href;
}
