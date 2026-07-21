export async function getStoredSession(): Promise<string | null> {
  return new Promise((resolve) => {
    const request = indexedDB.open("origami-unfold", 1);

    request.onsuccess = () => {
      const db = request.result;

      const tx = db.transaction("metadata", "readonly");

      const get = tx.objectStore("metadata").get("session");

      get.onsuccess = () => {
        resolve(get.result ?? null);
        db.close();
      };

      get.onerror = () => {
        resolve(null);
        db.close();
      };
    };
  });
}

export async function setStoredSession(session: string) {
  return new Promise<void>((resolve) => {
    const request = indexedDB.open("origami-unfold", 1);

    request.onsuccess = () => {
      const db = request.result;

      const tx = db.transaction("metadata", "readwrite");

      tx.objectStore("metadata").put(session, "session");

      tx.oncomplete = () => {
        db.close();
        resolve();
      };
    };
  });
}