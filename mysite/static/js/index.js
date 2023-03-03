const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const date = new Date().toLocaleDateString('ar-EG', options); // 'ar-EG' for Arabic (Egypt) locale
        document.getElementById('today-date').innerHTML = date;
