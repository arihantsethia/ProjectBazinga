function validateform()
{

	var username=document.forms["register"]["username"].value;
	var password=document.forms["register"]["password"].value;
	var cofpassword=document.forms["register"]["cofpassword"].value;
	var mail=document.forms["register"]["email"].value;
	var name=document.forms["register"]["name"].value;
	var atpos=mail.indexOf("@");
	var dotpos=mail.lastIndexOf(".");
	var flag=0;
	if (username==null || username=="")
	{
		register.username.style.borderColor='red';
		register.username.focus();
		flag=1;
	}
	else
	{
		register.username.style.borderColor='green';
	}
	
	if (password==null || password=="")
	{
		register.password.style.borderColor='red';
		register.password.focus();
		flag=1;
	}
	else
	{
		register.password.style.borderColor='green';
	}
	
	if (cofpassword==null || cofpassword=="")
	{
		register.cofpassword.style.borderColor='red';
		register.cofpassword.focus();
		flag=1;
	}
	else
	{
		register.cofpassword.style.borderColor='green';
	}
	
	if(cofpassword!="" && password!="")
	{
		if (password!=cofpassword)
		{
			register.password.style.borderColor='red';
			register.cofpassword.style.borderColor='red';
			flag=1;
		}
		else
		{
			register.cofpassword.style.borderColor='green';
		}
	}
	
	
	if (mail==null || mail=="")
	{
		register.email.style.borderColor='red';
		register.email.focus();
		flag=1;
	}
	else
	{
		if (atpos<1 || dotpos<atpos+2 || dotpos+2>=mail.length)
  		{
  			register.email.style.borderColor='red';
  			flag=1;
  		}
  		else
  		{
			register.email.style.borderColor='green';
		}
	}
	
	if (name==null || name=="")
	{
		register.name.style.borderColor='red';
		register.name.focus();
		flag=1;
	}
	else
	{
		register.name.style.borderColor='green';
	}
	
  	if (flag==1)
  	{
  		return false;
  	}
}

