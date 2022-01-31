// var inputs = document.getElementsByClassName('wprm-recipe-template-edited-cutout-container')
// var bagButton = null;
// console.log(inputs[0])
// console.log(inputs[0].innerText)
// for(var i = 0; i < inputs.length-1; i++) {
//     if(inputs[i].title.toLowerCase() == 'add to bag') {
//         inputs[i].style.backgroundColor = 'red'
//         bagButton = inputs[i]
//         inputs[i].innerHTML = 'Add to Bag (You dont need it) &#129324'
//         // inputs[i].addEventListener('click', function() {
//         //     alert('damn');
//         // });
//     }
// }

chrome.runtime.onMessage.addListener((msg, sender, response) => {
    // First, validate the message's structure.
    if ((msg.from === 'popup')) {
      // Collect the necessary data. 
      var inputs = document.getElementsByClassName('wprm-recipe-template-edited-cutout-container')
      let recipeData = inputs[0].innerHTML
      console.log(recipeData)
      
      let recipeInfo = {
          recipe: recipeData
      } 

    //   var domInfo = {
    //     total: document.querySelectorAll('*').length,
    //     inputs: document.querySelectorAll('input').length,
    //     buttons: document.querySelectorAll('button').length,
    //   };
  
      // Directly respond to the sender (popup), 
      // through the specified callback.
      response(recipeInfo);
    }
  });