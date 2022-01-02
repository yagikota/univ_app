function handleReplyButton(responseId) {
    const replyFormContainer = document.getElementById(`reply-form-container-${responseId}`);
    if (replyFormContainer) {
        var class_str = replyFormContainer.className
        console.log(class_str)
        if (class_str.indexOf('hidden') !== -1) {
            console.log(replyFormContainer)
            replyFormContainer.className = 'reply-form-container ml-1 pl-1 border-left'
        } else {
            replyFormContainer.className = 'hidden reply-form-container ml-1 pl-1 border-left'
        }
    }
}

function handleShowReply(responseId) {
    const showreplyContainer = document.getElementById(`dropdown-${responseId}-show-reply`);
    if (showreplyContainer) {
        var class_str = showreplyContainer.className
        if (class_str.indexOf('hidden') != -1) {
            showreplyContainer.className = 'show-reply-container'
            document.getElementById(`show-hide-txt`).innerText = "非表示"

        } else {
            showreplyContainer.className = 'hidden show-reply-container'
            document.getElementById(`show-hide-txt`).innerText = "表示"
        }
    }
}
