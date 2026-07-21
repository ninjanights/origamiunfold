
export async function clearConversationDB(): Promise<void> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("origami-unfold", 1);

    request.onsuccess = () => {
      const db = request.result;

      const tx = db.transaction("conversation", "readwrite");

      tx.objectStore("conversation").delete("messages");

      tx.oncomplete = () => {
        db.close();
        resolve();
      };

      tx.onerror = () => {
        db.close();
        reject(tx.error);
      };
    };

    request.onerror = () => reject(request.error);
  });
}