function definicoes() {
    var x = document.getElementById("dropdown_definicoes");
      x.classList.toggle("is-active");
  }

  function notificacoes() {
    var x = document.getElementById("ver_notificacoes");
    if (x.className === "modal") {
      x.className = "modal is-active";
    } else {
      x.className = "modal";
    }
  }

  function openNotificacoes(evt, tipo_notificacao) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" is-active", "");
    }
    document.getElementById(tipo_notificacao).style.display = "block";
    evt.currentTarget.className += " is-active";
  }

  function my_special_notification_callback(data) {
    for (var i = 0; i < data.unread_list.length; i++) {
      document.getElementById("badge-inject").style.display = "";
      document.getElementById("sem-mensagens").style.display = "none";
      document.getElementById("sem-notificacoes").style.display = "none";
    }
  }


function lista_notificacoes(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            var message = "";
            if (typeof item.id !== 'undefined') {
                      
                message += '<div data-tooltip="Click para ver detalhes">';
                message += '<a href="'+detalhes_url_notificacoes(item)+'" class="panel-block" style=" background: Gainsboro; ">';
                if (typeof item.level !== 'undefined') {
                    if (item.level === "info") {
                        message += '<span class="icon has-text-info"> ';
                        message += '  <i class="fas fa-info-circle"></i> ';
                        message += '  </span>';
                    } else if (item.level === "success") {
                        message += '<span class="icon has-text-success"> ';
                        message += ' <i class="fas fa-check-square"></i> ';
                        message += '  </span>';
                    } else if (item.level === "warning") {
                        message += '<span class="icon has-text-warning">';
                        message += '  <i class="fas fa-exclamation-triangle"></i> ';
                        message += '  </span>';
                    } else {
                        message += '<span class="icon has-text-danger"> ';
                        message += '  <i class="fas fa-ban"></i> ';
                        message += '  </span>';
                    }
                }
                if (typeof item.description !== 'undefined') {
                    message += '<p><strong>' + item.description + '</strong></p>';
                }
            }
            message += ' </a> </div> ';
            return message;
        }).join('')

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
        }
    }
}
  