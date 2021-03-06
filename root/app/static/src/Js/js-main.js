/* Pagination btn functionality */
class Pagination {
  constructor(announcements, ac_per_page, isInAuth) {
    this._aList = document.getElementById("aList");
    this._ac_per_page = ac_per_page;
    this._announcements = announcements;
    this._isInAuth = isInAuth;
    console.log(announcements);
    // Create idMapping and pass it to Annoucements object
    this.idMapping = {};
    this._announcements.forEach((a, index) => {
      this.idMapping[index] = { id: a.id }
    });
  }

  _createListItem(date, content, title, index) {
    const dateObj = new Date(date);
    const datestr = `民國${dateObj.getFullYear() - 1911}/${dateObj.getMonth()}/${dateObj.getDate()}`;
    if (!this._isInAuth) {
      return `<li class="announcement__list__item">
      <div class="announcement__list__item__heading">
        <span> ${datestr} </span>
        <span> ${title} </span>
      </div>
      <p class="announcement__list__item__p"> ${content} </p>
      </li>`;
    } else {
      return `<li class="announcement__list__item">
      <div class="announcement__list__item__heading">
        <span> ${datestr} </span>
        <span> ${title} </span>
      </div>
      <p class="announcement__list__item__p"> ${content} </p>
      <svg viewBox="0 0 500 500" height="30" width="30" class="announcement__list__item__close" id="item-${index}">
        <path d="m415.402344 495.421875-159.40625-159.410156-159.40625 159.410156c-22.097656 22.09375-57.921875 22.09375-80.019532 0-22.09375-22.097656-22.09375-57.921875 0-80.019531l159.410157-159.40625-159.410157-159.40625c-22.09375-22.097656-22.09375-57.921875 0-80.019532 22.097657-22.09375 57.921876-22.09375 80.019532 0l159.40625 159.410157 159.40625-159.410157c22.097656-22.09375 57.921875-22.09375 80.019531 0 22.09375 22.097657 22.09375 57.921876 0 80.019532l-159.410156 159.40625 159.410156 159.40625c22.09375 22.097656 22.09375 57.921875 0 80.019531-22.097656 22.09375-57.921875 22.09375-80.019531 0zm0 0" fill="#e76e54"/>
      </svg>
      </li>`;
    }
  }

  _createListItems(currentPage) {
    let start = currentPage * this._ac_per_page;
    let end = start + this._ac_per_page > this._announcements.length ? this._announcements.length : start + this._ac_per_page;
    let listr = "";
    for (let i = start; i < end; i++) {
      listr = `${listr}${this._createListItem(
          this._announcements[i].date,
          this._announcements[i].content,
          this._announcements[i].title,
          i
        )}`;
    }
    return listr;
  }

  _renderOnePage(num) {
    const listr = this._createListItems(num);
    this._aList.innerHTML = listr;
  }

  renderInit() {
    window.addEventListener('load', () => {
      this._renderOnePage(0);
    });
  }

  addPagination() {
    const paginations = Array.from(document.querySelectorAll(".announcement__pagination__item"));
    /* 
      Use arrow function
      So this of this._renderOnePage will refer to the outer scope,
      which is the callback function inside forEach(),
      But the callback function inside forEach() is also an arrow function,
      so the this keyword will refer to the outer scope,
      which is addPagination(), and get the proper this binding
    */

    /* 
      paginations.forEach(function(p) {
        ......
      }, this);

      will also work since we pass this obj into forEach and bind the callback function to it
    */
    paginations.forEach((p) => {
      p.addEventListener("click", () => {
        this._renderOnePage(parseInt(p.innerHTML) - 1);
      })
    });
  }
}
