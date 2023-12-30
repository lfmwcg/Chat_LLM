function fetchSessionData() {
    fetch('/get_session_data')
        .then(response => response.json())
        .then(data => {
            const ul = document.querySelector('.left-panel ul');
            data.forEach(item => {
                const div = document.createElement('div');
                div.classList.add('li_session_div');
                const li = document.createElement('li');
                li.textContent = item[2];
                li.id = item[1];
                li.onclick = function () {
                    // 在此处添加处理点击事件的代码，可以使用li.id作为参数
                    fetchConversionData(li.id);
                };
                div.appendChild(li);
                ul.appendChild(div);
            });
        });
}

//fetchSessionData()

function addConversionItem(ul, userText, aiText) {
    const div = document.createElement('div');
    div.classList.add('li_conversion_div');
    const li_usr = document.createElement('li');
    li_usr.innerHTML = '<img src="static/user.png" alt="Icon" class="icon">' + userText;
    div.appendChild(li_usr);
    const li_ai = document.createElement('li');
    li_ai.innerHTML = '<img src="static/ai.png" alt="Icon" class="icon">' + aiText;
    div.appendChild(li_ai);

    const br = document.createElement('br');
    ul.appendChild(br);

    ul.appendChild(div);

    const chatProcess = document.querySelector('.chat-process');
    chatProcess.scrollTop = chatProcess.scrollHeight - chatProcess.clientHeight;
}

function clearInput() {
    document.getElementById('input-text').value = '';
}

function init_api_key() {
    const inputApiKey = document.cookie
        .split('; ')
        .find(row => row.startsWith('input_api_key='))
        .split('=')[1];

    document.getElementById('input-api-key').value = inputApiKey;
}

// 从flask后台接口获取session对话内容
function fetchConversionData(sessionId) {
    fetch(`/get_conversion_data?sessionId=${sessionId}`)
        .then(response => response.json())
        .then(data => {
            const ul = document.querySelector('.right-panel .conversion_ul');
            ul.innerHTML = '';
            data.forEach(item => {
                addConversionItem(ul, item[3], item[4]);
            });
        });

    // 滚动到最底部    
    const chatProcess = document.querySelector('.chat-process');
    chatProcess.scrollTop = chatProcess.scrollHeight - chatProcess.clientHeight;
}


function submitData() {
    var inputContent = document.getElementById('input-text').value;
    if (inputContent.trim() === '') {
        return;
    }
    // 将 inputContent 提交到后台处理
    // 例如使用 fetch 或者 XMLHttpRequest 发送数据到后台
    fetch('/usr_submit_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: inputContent }),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            const ul = document.querySelector('.right-panel .conversion_ul');
            addConversionItem(ul, inputContent, data.message);

            const chatProcess = document.querySelector('.chat-process');
            chatProcess.scrollTop = chatProcess.scrollHeight - chatProcess.clientHeight;

            clearInput();

        })
        .catch(error => {
            // 处理错误
            console.error('Error:', error);
        });


}


function proc_Data_front() {
    console.log("--enter proc_Data_front--");
    var input_api_key = document.getElementById('input-api-key').value;
    if (input_api_key.trim() === '') {
        alert('请输入API_KEY');
    }

    document.cookie = `input_api_key=${input_api_key}`;

    var inputContent = document.getElementById('input-text').value;
    if (inputContent.trim() === '') {
        return;
    }

    message = call_Gemini_Rest_API(inputContent, input_api_key);

}


function call_Gemini_Rest_API(inputContent, input_api_key) {

    // 构造对应的数据结构
    var postData = {
        contents: [
            {
                parts: [
                    {
                        text: ""
                    }
                ]
            }
        ]
    };

    // 访问和修改值
    postData.contents[0].parts[0].text = inputContent;


    fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + input_api_key, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // 告诉服务器发送的是 JSON 数据
        },
        body: JSON.stringify(postData), // 将对象转换为 JSON 字符串
    })
        .then((response) => {
            if (!response.ok) {
                console.log(error.message);
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('Server response:', data); // 在控制台中输出服务器的响应数据
            // 在这里处理服务器的响应
            //const parsedData = JSON.parse(data);
            const textValue = data.candidates[0].content.parts[0].text;
            console.log("120" + textValue);

            const ul = document.querySelector('.right-panel .conversion_ul');
            addConversionItem(ul, inputContent, textValue);

            clearInput();

            return textValue;
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

document.addEventListener('DOMContentLoaded', function () {
    // 在这里放置需要在页面加载完成后执行的代码
    console.log('页面加载完成！');
    init_api_key();

});