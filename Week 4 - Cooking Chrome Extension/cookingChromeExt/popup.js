
document.addEventListener('DOMContentLoaded', function() {
    var checkButton = document.getElementById('getrecipe');
    checkButton.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {from: "popup"}, function(response) {
                console.log(response.recipe);
                let recipe = document.createElement("p")
                newWindow = window.open("", null, "height=800,width=600,status=yes,toolbar=no,menubar=no,location=no");  
                newWindow.document.write("<html>")
                newWindow.document.write(response.recipe)
                newWindow.document.write("</html>")
            //   chrome.windows.create({tabId: tab.id,
            //                 focused: true,
            //                 type: "popup",
                            
            //             })
            // alert(response.recipe)
            });
          });
        console.log('recipe')
    }, false);
  }, false);