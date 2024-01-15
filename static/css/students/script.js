document.getElementById("addSubVideo").addEventListener("click", function () {
  const subVideoContainer = document.createElement("div");
  subVideoContainer.classList.add("subVideo");

  const titleLabel = document.createElement("label");
  titleLabel.textContent = "Title:";
  subVideoContainer.appendChild(titleLabel);

  const titleInput = document.createElement("input");
  titleInput.type = "text";
  titleInput.classList.add("subVideoTitle");
  titleInput.required = true;
  subVideoContainer.appendChild(titleInput);

  subVideoContainer.appendChild(document.createElement("br"));

  const descriptionLabel = document.createElement("label");
  descriptionLabel.textContent = "pdf Description:";
  subVideoContainer.appendChild(descriptionLabel);

  const descriptionTextarea = document.createElement("textarea");
  descriptionTextarea.classList.add("subVideoDescription");
  descriptionTextarea.required = true;
  subVideoContainer.appendChild(descriptionTextarea);

  subVideoContainer.appendChild(document.createElement("br"));

  const fileLabel = document.createElement("label");
  fileLabel.textContent = "File:";
  subVideoContainer.appendChild(fileLabel);

  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.classList.add("subVideoFile");
  fileInput.accept = "application/pdf";
  subVideoContainer.appendChild(fileInput);

  subVideoContainer.appendChild(document.createElement("br"));

  const removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.classList.add("removeSubVideo");
  removeButton.textContent = "Remove";
  removeButton.addEventListener("click", function () {
    subVideoContainer.remove();
  });
  subVideoContainer.appendChild(removeButton);

  document.getElementById("subVideosContainer").appendChild(subVideoContainer);
});

document
  .getElementById("videoForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const mainVideo = document.getElementById("mainVideo").files[0];
    const subVideos = Array.from(document.getElementsByClassName("subVideo"));

    const videoRow = document.createElement("tr");

    const mainVideoCell = document.createElement("td");
    mainVideoCell.textContent = mainVideo.name;
    videoRow.appendChild(mainVideoCell);

    const subVideosCell = document.createElement("td");
    subVideos.forEach(function (subVideo) {
      const subVideoTitle = subVideo.querySelector(".subVideoTitle").value;
      const subVideoDescription = subVideo.querySelector(
        ".subVideoDescription"
      ).value;
      const subVideoFile = subVideo.querySelector(".subVideoFile").files[0];

      const subVideoEntry = document.createElement("div");
      subVideoEntry.innerHTML =
        "<strong>Title:</strong> " +
        subVideoTitle +
        "<br><strong>Description:</strong> " +
        subVideoDescription +
        "<br>";

      if (subVideoFile) {
        subVideoEntry.innerHTML +=
          "<strong>File:</strong> " + subVideoFile.name + "<br>";
      }

      subVideosCell.appendChild(subVideoEntry);
    });
    videoRow.appendChild(subVideosCell);

    const actionsCell = document.createElement("td");
    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.addEventListener("click", function () {
      // Implement the edit functionality here
      console.log("Edit button clicked");
    });
    actionsCell.appendChild(editButton);
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", function () {
      videoRow.remove();
    });
    actionsCell.appendChild(deleteButton);

    videoRow.appendChild(actionsCell);

    document
      .getElementById("videoTable")
      .getElementsByTagName("tbody")[0]
      .appendChild(videoRow);

    document.getElementById("videoForm").reset();
  });
