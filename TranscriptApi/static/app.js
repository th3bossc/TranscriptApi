function youtube_video_id(url){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? match[7] : false;
}


// Theme implementation

const theme = localStorage.getItem('theme');
const navbar_bg = localStorage.getItem('navbar-bg');
const navbar_color = localStorage.getItem('navbar-color');
const button_content = localStorage.getItem('button-content');


const themeButton = document.getElementById('theme');
const body = document.body;
const nav = document.getElementById('navbar');

body.classList.add(theme || 'light');
nav.classList.add(navbar_bg || 'bg-light');
nav.classList.add(navbar_color || 'navbar-light')
themeButton.innerHTML = button_content || '<i class="bi bi-moon-fill"></i> Toggle Theme';


themeButton.onclick = () => {
    if (body.classList.contains('light')) {
        body.classList.replace('light', 'dark');
        nav.classList.replace('bg-light', 'bg-dark');
        nav.classList.replace('navbar-light', 'navbar-dark'); 
        themeButton.innerHTML = '<i class="bi bi-brightness-high-fill"></i> Toggle Theme'

        localStorage.setItem('theme', 'dark');
        localStorage.setItem('navbar-bg', 'bg-dark');
        localStorage.setItem('navbar-color', 'navbar-dark');
        localStorage.setItem('button-content', themeButton.innerHTML);
    }
    else {
        body.classList.replace('dark', 'light');
        nav.classList.replace('bg-dark', 'bg-light');
        nav.classList.replace('navbar-dark', 'navbar-light');
        themeButton.innerHTML = '<i class="bi bi-moon-fill"></i> Toggle Theme';

        localStorage.setItem('theme', 'light');
        localStorage.setItem('navbar-bg', 'bg-light');
        localStorage.setItem('navbar-color', 'navbar-light');
        localStorage.setItem('button-content', themeButton.innerHTML);
    }
}

// darkButton.onclick = () => {
//     body.classList.replace('light', 'dark');
//     nav.classList.replace('bg-light', 'bg-dark');
//     nav.classList.replace('navbar-light', 'navbar-dark'); 
//     darkButton.classList.add('active');
//     darkButton.classList.add('disabled');
//     lightButton.classList.remove('active');
//     lightButton.classList.remove('disabled'); 
// };

// lightButton.onclick = () => {
//     body.classList.replace('dark', 'light');
//     nav.classList.replace('bg-dark', 'bg-light');
//     nav.classList.replace('navbar-dark', 'navbar-light');   
//     lightButton.classList.add('active');
//     lightButton.classList.add('disabled');     
//     darkButton.classList.remove('active');
//     darkButton.classList.remove('disabled'); 
// };


const main_content = document.getElementById('main-content');
const video_title = document.getElementById('video-title');
const video_summary = document.getElementById('video-summary');

const button = document.getElementById('submit-btn');
const form = document.getElementById('url-form');
const url = document.getElementById('url')

async function getApiData(video_id) {
    const response = await fetch('http://localhost:5000/video_api/' + video_id);
    const jsonData = await response.json();

    console.log(jsonData);
    video_title.innerHTML = jsonData['title'];
    return video_summary.innerHTML = jsonData['summary'];

}



form.addEventListener('submit', (e) => {
    e.preventDefault();
    video_url = url.value;  
    if (video_url == "")
        return;
    video_id = youtube_video_id(video_url);
    video_title.innerHTML = 'Summarizing...';
    console.log(main_content.classList);
    //main_content.classList.remove('visually-hidden');
    main_content.style.clipPath = 'circle(200% at 50% 50%)';
    video_summary.innerHTML = '<div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"> \
    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div> \
  </div>';
    if (video_id == false) {
        video_title.innerHTML = '[Error]';
        video_summary.innerHTML = 'Invalid video URL';
        return;
    }
    try {
        getApiData(video_id);
    }
    catch {
        video_title.innerHTML = '[Error]'
        video_summary.innerHTML = 'Error Video not found';
    }
}); 

