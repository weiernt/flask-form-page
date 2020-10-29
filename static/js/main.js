
const subscription_obj = document.getElementById('subscription-price');
const original_subscription_price_text = subscription_obj.textContent;

const carbon_footprint_obj = document.getElementById('carbon-footprint');
const original_carbon_footprint_text = carbon_footprint_obj.textContent;

// Look for the <input> tag ids'
// DOM objects from the form data, should have same Id as their identifier/variable name
// These var names were straight copy pasted from ucalc.pro's formula
const B   = document.getElementById('integer_fields-B');     //Integer fields
const AH	= document.getElementById('integer_fields-AH');
const	AI  = document.getElementById('integer_fields-AI');
const	F   = document.getElementById('integer_fields-F');
const	D	  = document.getElementById('integer_fields-D');
const	H	  = document.getElementById('integer_fields-H');
const	M	  = document.getElementById('integer_fields-M');
const	AF  = document.getElementById('integer_fields-AF');
const	L	  = document.getElementById('integer_fields-L');
const	K	  = document.getElementById('integer_fields-K');
const	J	  = document.getElementById('integer_fields-J');
const	I	  = document.getElementById('integer_fields-I');

const	R	  = document.getElementById('radio_fields-R');   // RadioFields 
const	U	  = document.getElementById('radio_fields-U');
const	X	  = document.getElementById('radio_fields-X');
const	AA  = document.getElementById('radio_fields-AA');
const	AB	= document.getElementById('radio_fields-AB');  
console.log("hello");
console.log(B);
form_obj_list = [B, AH, AI, F, D, H, M, AF, L, K, J, I, R, U, X, AA, AB];
// radio_obj_list = [R, U, X, AA, AB];


// Adds the event listener to all (form) objects to check if their value changed
for (var i=0;i<form_obj_list.length;i++) {
  form_obj_list[i].addEventListener('input', updateValue);
}


function updateValue(e) {
  // Should update both carbon_footprint value and the subscription price


  // Detected that some form component's value changed, so obtain all form's
  // value again, then recalculate the carbon value and subscription price 
  const B_val   = Number(B.value);                // All here are IntegerFields
  const AH_val	= Number(AH.value);
  const	AI_val  = Number(AI.value);
  const	F_val   = Number(F.value);
  const	D_val	  = Number(D.value);
  const	H_val	  = Number(H.value);
  const	M_val	  = Number(M.value);
  const	AF_val  = Number(AF.value);
  const	L_val	  = Number(L.value);
  const	K_val	  = Number(K.value);
  const	J_val	  = Number(J.value);
  const	I_val	  = Number(I.value);
  
  console.log(document.getElementsByName('radio_fields-AB'));

  // below are radio, search ByName since they have <tr> stuff so search by
  // name searches for the TOP <ul> tag
  // Note I'm not using the objects R, X, AA etc since they search by Id, not name
  const	R_val	  = Number(getCheckedValue(document.getElementsByName('radio_fields-R')));  // RadioFields
  const	U_val	  = Number(getCheckedValue(document.getElementsByName('radio_fields-U')));
  const	X_val	  = Number(getCheckedValue(document.getElementsByName('radio_fields-X')));
  const	AA_val  = Number(getCheckedValue(document.getElementsByName('radio_fields-AA')));
  const	AB_val	= Number(getCheckedValue(document.getElementsByName('radio_fields-AB')));

  // If formula is changed in python file you HAVE TO change it here as well, and vice versa
  const carbon_footprint_value = B_val*0.000174+D_val*0.00012+F_val*0.00002+((AH_val*0.00009747)/189)+((AI_val*0.0001111)/150)+(H_val*0.0084)+(I_val*0.00044)+(J_val*0.00112)+(K_val*0.00063)+(L_val*0.00072)+(M_val*0.00024)+(AF_val*0.00002)+(R_val+U_val+X_val)*0.00102+(AA_val*1.6917);
  const subscription_price_value = carbon_footprint_value * AB_val * 25 * 1.29 / 12;

  // console.log(" carbon_footprint_value = " + B_val + AH_val + AI_val);
  // console.log(document.getElementById('AB'))

  const subscription_obj = document.getElementById('subscription-price');
  const carbon_footprint_obj = document.getElementById('carbon-footprint');

  // add to original text to display the price/values
  carbon_footprint_obj.textContent = original_carbon_footprint_text + carbon_footprint_value.toFixed(2);
  subscription_obj.textContent = original_subscription_price_text + subscription_price_value.toFixed(2);

}

function getCheckedValue(obj) {
  // takes in a DOM object that should be of type="radio"
  // length indicates the amount of choices for the radio

  // finds the choice that is "checked", then gets that value (this value is set in main.py, using WTForms)
  for (var i=0;i<obj.length; i++) {
    if (obj[i].checked) {
      return obj[i].value;
    }
  }

  // return 1 to not print out NaN in the footer, but can sometimes result in negative prices when form isnt fully filled out.
  return 1; 
}