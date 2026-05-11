"use client";

export type StoredUploadImageRecord = {
  id: string;
  name: string;
  type: string;
  sizeBytes: number;
  createdAt: string;
  uploadedImageId?: string | null;
  blob: Blob;
};

const DATABASE_NAME = "stylematch-recent-uploads";
const STORE_NAME = "upload_images";
const DATABASE_VERSION = 1;
const MAX_RECENT_UPLOADS = 8;

function isIndexedDbAvailable(): boolean {
  return typeof window !== "undefined" && typeof window.indexedDB !== "undefined";
}

function createRecordId(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }

  return `upload-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function openDatabase(): Promise<IDBDatabase | null> {
  if (!isIndexedDbAvailable()) {
    return Promise.resolve(null);
  }

  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(DATABASE_NAME, DATABASE_VERSION);

    request.onerror = () => {
      reject(request.error ?? new Error("최근 업로드 저장소를 열지 못했습니다."));
    };

    request.onupgradeneeded = () => {
      const database = request.result;
      if (!database.objectStoreNames.contains(STORE_NAME)) {
        database.createObjectStore(STORE_NAME, {
          keyPath: "id",
        });
      }
    };

    request.onsuccess = () => {
      resolve(request.result);
    };
  });
}

async function withStore<T>(
  mode: IDBTransactionMode,
  operation: (store: IDBObjectStore) => Promise<T>,
): Promise<T | null> {
  const database = await openDatabase();
  if (!database) {
    return null;
  }

  const transaction = database.transaction(STORE_NAME, mode);
  const store = transaction.objectStore(STORE_NAME);

  try {
    return await operation(store);
  } finally {
    database.close();
  }
}

function wrapRequest<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => {
      resolve(request.result);
    };
    request.onerror = () => {
      reject(request.error ?? new Error("최근 업로드 저장소 요청이 실패했습니다."));
    };
  });
}

async function pruneOverflow(store: IDBObjectStore): Promise<void> {
  const allRecords = (await wrapRequest(store.getAll())) as StoredUploadImageRecord[];
  const overflowRecords = [...allRecords]
    .sort((left, right) => right.createdAt.localeCompare(left.createdAt))
    .slice(MAX_RECENT_UPLOADS);

  await Promise.all(overflowRecords.map((record) => wrapRequest(store.delete(record.id))));
}

export async function saveStoredUploadImage(
  image: Blob,
  options: {
    id?: string;
    name: string;
    type: string;
    createdAt?: string;
    uploadedImageId?: string | null;
  },
): Promise<string | null> {
  const nextRecordId = options.id ?? createRecordId();
  const createdAt = options.createdAt ?? new Date().toISOString();

  return withStore("readwrite", async (store) => {
    const record: StoredUploadImageRecord = {
      id: nextRecordId,
      name: options.name,
      type: options.type,
      sizeBytes: image.size,
      createdAt,
      uploadedImageId: options.uploadedImageId ?? null,
      blob: image,
    };

    await wrapRequest(store.put(record));
    await pruneOverflow(store);
    return nextRecordId;
  });
}

export async function listStoredUploadImages(): Promise<StoredUploadImageRecord[]> {
  const records = await withStore("readonly", async (store) => {
    const storedRecords = (await wrapRequest(store.getAll())) as StoredUploadImageRecord[];
    return storedRecords.sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  });

  return records ?? [];
}

export async function getStoredUploadImage(id: string): Promise<StoredUploadImageRecord | null> {
  const record = await withStore("readonly", async (store) => {
    return (await wrapRequest(store.get(id))) as StoredUploadImageRecord | undefined;
  });

  return record ?? null;
}

export async function getStoredUploadImageByUploadedImageId(
  uploadedImageId: string,
): Promise<StoredUploadImageRecord | null> {
  const matchingRecords = await withStore("readonly", async (store) => {
    const storedRecords = (await wrapRequest(store.getAll())) as StoredUploadImageRecord[];
    return storedRecords
      .filter((record) => record.uploadedImageId === uploadedImageId)
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  });

  return matchingRecords?.[0] ?? null;
}

export async function deleteStoredUploadImage(id: string): Promise<void> {
  await withStore("readwrite", async (store) => {
    await wrapRequest(store.delete(id));
  });
}
