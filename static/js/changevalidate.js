function validatechange()
{

	var username=document.forms["change"]["username"].value;
	var password=document.forms["change"]["password"].value;
	var newpassword=document.forms["change"]["newpassword"].value;
	var cofpassword=document.forms["change"]["cofpassword"].value;
	var flag=0;
	if (username==null || username=="")
	{
		change.username.style.borderColor='red';
		change.username.focus();
		flag=1;
	}
	else
	{
		change.username.style.borderColor='green';
	}
	
	if (password==null || password=="")
	{
		change.password.style.borderColor='red';
		change.password.focus();
		flag=1;
	}
	else
	{
		change.password.style.borderColor='green';
	}
	
	if (newpassword==null || newpassword=="")
	{	
		change.newpassword.style.borderColor='red';
		change.newpassword.focus();
		flag=1;
	}
	else
	{
		change.newpassword.style.borderColor='green';
	}
	
	if (cofpassword==null || cofpassword=="")
	{
		change.cofpassword.style.borderColor='red';
		change.cofpassword.focus();
		flag=1;
	}
	else
	{
		change.cofpassword.style.borderColor='green';
	}
	if(cofpassword!="" && newpassword!="")
	{
		if (newpassword!=cofpassword)
		{
			change.newpassword.style.borderColor='red';
			change.cofpassword.style.borderColor='red';
			flag=1;
		}
		else
		{
			change.cofpassword.style.borderColor='green';
			change.newpassword.style.borderColor='green';
		}
	}
	
  	if (flag==1)
  	{
  		return false;
  	}
}

