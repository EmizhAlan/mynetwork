document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const postId = btn.dataset.id;
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById(`likes-${postId}`).innerText = data.likes_count;
                btn.innerText = data.liked ? '❤️' : '🤍';
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
