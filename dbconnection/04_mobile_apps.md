# モバイルアプリケーション向けデータベース接続ベストプラクティス

## 概要

このガイドは、iOS/Androidモバイルアプリケーション向けのデータベース接続とデータ管理のベストプラクティスを提供します。オフライン対応、同期戦略、効率的なデータ転送に焦点を当てています。

### ターゲットアプリケーション

- iOSアプリケーション（Swift, Objective-C）
- Androidアプリケーション（Kotlin, Java）
- クロスプラットフォームアプリ（React Native, Flutter, Xamarin）
- オフライン機能が必要なアプリ
- リアルタイム同期が必要なアプリ

## レイテンシ最適化

### オフライン対応と同期戦略

```swift
// Swift (iOS) - Core Data + バックグラウンド同期
import CoreData
import Foundation

class DataSyncManager {
    private let context: NSManagedObjectContext
    private let apiClient: APIClient
    
    init(context: NSManagedObjectContext, apiClient: APIClient) {
        self.context = context
        self.apiClient = apiClient
    }
    
    func syncInBackground() {
        // バックグラウンドで同期
        DispatchQueue.global(qos: .background).async { [weak self] in
            guard let self = self else { return }
            
            // 1. ローカルの変更を取得
            let localChanges = self.getLocalChanges()
            
            // 2. サーバーに送信
            self.uploadChanges(localChanges)
            
            // 3. サーバーから最新データを取得
            self.downloadLatestChanges()
        }
    }
    
    private func getLocalChanges() -> [Change] {
        // ローカルで変更されたが未同期のデータを取得
        let request = NSFetchRequest<Change>(entityName: "Change")
        request.predicate = NSPredicate(format: "synced == NO")
        return try! context.fetch(request)
    }
    
    private func uploadChanges(_ changes: [Change]) {
        // バッチでアップロード
        let batch = changes.map { $0.toJSON() }
        apiClient.post("/api/sync/upload", body: batch) { result in
            switch result {
            case .success:
                // 同期済みマーク
                changes.forEach { $0.synced = true }
                try? self.context.save()
            case .failure(let error):
                print("Sync failed: \(error)")
            }
        }
    }
    
    private func downloadLatestChanges() {
        // 最後の同期時刻を取得
        let lastSync = UserDefaults.standard.object(forKey: "lastSync") as? Date ?? Date.distantPast
        
        apiClient.get("/api/sync/download?since=\(lastSync.timeIntervalSince1970)") { result in
            switch result {
            case .success(let data):
                self.applyRemoteChanges(data)
            case .failure(let error):
                print("Download failed: \(error)")
            }
        }
    }
}
```

```kotlin
// Kotlin (Android) - Room + WorkManager
import androidx.room.*
import androidx.work.*

@Entity
data class User(
    @PrimaryKey val id: Int,
    val email: String,
    val username: String,
    @ColumnInfo(name = "synced") val synced: Boolean = false,
    @ColumnInfo(name = "updated_at") val updatedAt: Long = System.currentTimeMillis()
)

@Dao
interface UserDao {
    @Query("SELECT * FROM user WHERE synced = 0")
    suspend fun getUnsyncedUsers(): List<User>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)
    
    @Update
    suspend fun updateUser(user: User)
}

class SyncWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        return try {
            val db = AppDatabase.getDatabase(applicationContext)
            val apiClient = APIClient()
            
            // 未同期データを取得
            val unsyncedUsers = db.userDao().getUnsyncedUsers()
            
            // アップロード
            apiClient.uploadUsers(unsyncedUsers)
            
            // ダウンロード
            val remoteUsers = apiClient.downloadUsers()
            remoteUsers.forEach { db.userDao().insertUser(it) }
            
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}

// 定期的な同期の設定
val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()
    )
    .build()

WorkManager.getInstance(context).enqueue(syncRequest)
```

### 効率的なデータ転送

```python
# バックエンドAPI - 差分同期
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/sync/download', methods=['GET'])
def download_changes():
    """差分データをダウンロード"""
    since = request.args.get('since', type=float)
    since_date = datetime.fromtimestamp(since) if since else datetime.min
    
    # 変更されたデータのみを取得
    changes = db.session.query(User).filter(
        User.updated_at > since_date
    ).all()
    
    return jsonify({
        'changes': [user.to_dict() for user in changes],
        'timestamp': datetime.utcnow().timestamp()
    })

@app.route('/api/sync/upload', methods=['POST'])
def upload_changes():
    """変更をアップロード"""
    changes = request.json
    
    for change in changes:
        user = db.session.query(User).filter_by(id=change['id']).first()
        if user:
            # 競合解決（Last Write Wins）
            if change['updated_at'] > user.updated_at:
                user.update_from_dict(change)
        else:
            # 新規作成
            user = User.from_dict(change)
            db.session.add(user)
    
    db.session.commit()
    return jsonify({'status': 'success'})
```

## 経済的最適化

### API経由の接続とデータ転送最適化

```swift
// データ圧縮とバッチ処理
class OptimizedAPIClient {
    func uploadBatch(_ items: [DataItem], completion: @escaping (Result<Void, Error>) -> Void) {
        // 1. データを圧縮
        let jsonData = try! JSONEncoder().encode(items)
        let compressed = try! (jsonData as NSData).compressed(using: .lzfse)
        
        // 2. バッチでアップロード
        var request = URLRequest(url: URL(string: "https://api.example.com/sync")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("gzip", forHTTPHeaderField: "Content-Encoding")
        request.httpBody = compressed as Data
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
            } else {
                completion(.success(()))
            }
        }.resume()
    }
}
```

```kotlin
// Android - データ転送の最適化
class OptimizedAPIClient {
    suspend fun uploadBatch(items: List<DataItem>): Result<Unit> {
        return try {
            // JSONに変換
            val json = Gson().toJson(items)
            
            // 圧縮
            val compressed = json.toByteArray().gzip()
            
            // アップロード
            val request = Request.Builder()
                .url("https://api.example.com/sync")
                .post(compressed.toRequestBody("application/json".toMediaType()))
                .addHeader("Content-Encoding", "gzip")
                .build()
            
            val response = httpClient.newCall(request).execute()
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Upload failed"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// Gzip圧縮の拡張関数
fun ByteArray.gzip(): ByteArray {
    val bos = ByteArrayOutputStream()
    GZIPOutputStream(bos).use { it.write(this) }
    return bos.toByteArray()
}
```

### コスト削減戦略

1. **差分同期**: 変更されたデータのみを転送
2. **データ圧縮**: Gzip、LZ4などの圧縮を使用
3. **バッチ処理**: 複数の変更をまとめて送信
4. **キャッシング**: 頻繁にアクセスするデータをローカルにキャッシュ
5. **オフライン優先**: ネットワーク使用量を最小化

## セキュリティ

### トークンベース認証

```swift
// JWT認証の実装
import JWTKit

class AuthenticationManager {
    private let keychain = Keychain(service: "com.example.app")
    
    func authenticate(email: String, password: String, completion: @escaping (Result<String, Error>) -> Void) {
        let credentials = ["email": email, "password": password]
        
        apiClient.post("/api/auth/login", body: credentials) { result in
            switch result {
            case .success(let response):
                if let token = response["token"] as? String {
                    // トークンをKeychainに保存
                    try? self.keychain.set(token, key: "auth_token")
                    completion(.success(token))
                }
            case .failure(let error):
                completion(.failure(error))
            }
        }
    }
    
    func getAuthToken() -> String? {
        return try? keychain.get("auth_token")
    }
    
    func addAuthHeader(to request: inout URLRequest) {
        if let token = getAuthToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
    }
}
```

```kotlin
// Android - セキュアストレージ
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class SecureTokenStorage(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()
    
    private val sharedPreferences = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    
    fun saveToken(token: String) {
        sharedPreferences.edit()
            .putString("auth_token", token)
            .apply()
    }
    
    fun getToken(): String? {
        return sharedPreferences.getString("auth_token", null)
    }
}
```

### エンドツーエンド暗号化

```swift
// データの暗号化
import CryptoKit

class EncryptionManager {
    private let key: SymmetricKey
    
    init() {
        // キーをKeychainから取得または生成
        if let keyData = Keychain.shared.get("encryption_key"),
           let key = try? SymmetricKey(data: keyData) {
            self.key = key
        } else {
            self.key = SymmetricKey(size: .bits256)
            try? Keychain.shared.set(key.withUnsafeBytes { Data($0) }, key: "encryption_key")
        }
    }
    
    func encrypt(_ data: Data) throws -> Data {
        let sealedBox = try AES.GCM.seal(data, using: key)
        return sealedBox.combined!
    }
    
    func decrypt(_ encryptedData: Data) throws -> Data {
        let sealedBox = try AES.GCM.SealedBox(combined: encryptedData)
        return try AES.GCM.open(sealedBox, using: key)
    }
}
```

## UX最適化

### オフライン機能

```swift
// オフライン対応のデータアクセス
class OfflineDataManager {
    private let context: NSManagedObjectContext
    private let networkMonitor = NWPathMonitor()
    
    init(context: NSManagedObjectContext) {
        self.context = context
        
        // ネットワーク状態を監視
        networkMonitor.pathUpdateHandler = { [weak self] path in
            if path.status == .satisfied {
                self?.syncInBackground()
            }
        }
        networkMonitor.start(queue: DispatchQueue.global())
    }
    
    func getUser(id: Int, completion: @escaping (User?) -> Void) {
        // まずローカルから取得
        let request = NSFetchRequest<User>(entityName: "User")
        request.predicate = NSPredicate(format: "id == %d", id)
        
        if let user = try? context.fetch(request).first {
            completion(user)
            
            // バックグラウンドで最新データを取得
            if networkMonitor.currentPath.status == .satisfied {
                fetchLatestUser(id: id)
            }
        } else {
            // ローカルにない場合はネットワークから取得
            if networkMonitor.currentPath.status == .satisfied {
                fetchUserFromNetwork(id: id, completion: completion)
            } else {
                completion(nil)
            }
        }
    }
}
```

### バックグラウンド同期

```kotlin
// Android - バックグラウンド同期
class BackgroundSyncService : IntentService("BackgroundSyncService") {
    override fun onHandleIntent(intent: Intent?) {
        val syncManager = SyncManager(applicationContext)
        
        // ネットワーク接続を確認
        val connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return
        
        val capabilities = connectivityManager.getNetworkCapabilities(network)
        if (capabilities?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) == true) {
            // Wi-Fi接続時のみ同期（モバイルデータを節約）
            if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) {
                syncManager.syncAll()
            }
        }
    }
}

// 定期的な同期の設定
val syncIntent = Intent(context, BackgroundSyncService::class.java)
val syncPendingIntent = PendingIntent.getService(
    context, 0, syncIntent, PendingIntent.FLAG_UPDATE_CURRENT
)

val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
alarmManager.setInexactRepeating(
    AlarmManager.ELAPSED_REALTIME_WAKEUP,
    SystemClock.elapsedRealtime() + 15 * 60 * 1000, // 15分後
    15 * 60 * 1000, // 15分ごと
    syncPendingIntent
)
```

## データ保存戦略

### ローカルデータベース

```swift
// iOS - Core Data
import CoreData

class CoreDataStack {
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "DataModel")
        container.loadPersistentStores { description, error in
            if let error = error {
                fatalError("Core Data error: \(error)")
            }
        }
        return container
    }()
    
    var context: NSManagedObjectContext {
        return persistentContainer.viewContext
    }
    
    func save() {
        if context.hasChanges {
            try? context.save()
        }
    }
}
```

```kotlin
// Android - Room
import androidx.room.*

@Database(entities = [User::class, Post::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun postDao(): PostDao
    
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null
        
        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                .enableMultiInstanceInvalidation()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
```

### Realm（クロスプラットフォーム）

```swift
// Swift - Realm
import RealmSwift

class RealmDataManager {
    private let realm: Realm
    
    init() {
        realm = try! Realm()
    }
    
    func saveUser(_ user: User) {
        try! realm.write {
            realm.add(user, update: .modified)
        }
    }
    
    func getUser(id: Int) -> User? {
        return realm.object(ofType: User.self, forPrimaryKey: id)
    }
    
    func observeUsers(completion: @escaping ([User]) -> Void) {
        let users = realm.objects(User.self)
        let token = users.observe { changes in
            completion(Array(users))
        }
        // トークンを保持して後で無効化
    }
}
```

```kotlin
// Kotlin - Realm
import io.realm.Realm
import io.realm.RealmConfiguration

class RealmDataManager {
    private val realm: Realm
    
    init {
        val config = RealmConfiguration.Builder()
            .name("app.realm")
            .schemaVersion(1)
            .build()
        realm = Realm.getInstance(config)
    }
    
    fun saveUser(user: User) {
        realm.executeTransaction { realm ->
            realm.insertOrUpdate(user)
        }
    }
    
    fun getUser(id: Int): User? {
        return realm.where(User::class.java)
            .equalTo("id", id)
            .findFirst()
    }
}
```

### クラウドデータベース（BaaS）

```swift
// Firebase Realtime Database
import FirebaseDatabase

class FirebaseDataManager {
    private let ref = Database.database().reference()
    
    func saveUser(_ user: User) {
        ref.child("users").child("\(user.id)").setValue(user.toDictionary())
    }
    
    func observeUser(id: Int, completion: @escaping (User?) -> Void) {
        ref.child("users").child("\(id)").observe(.value) { snapshot in
            if let dict = snapshot.value as? [String: Any] {
                let user = User.fromDictionary(dict)
                completion(user)
            }
        }
    }
}
```

```kotlin
// Android - Firebase
import com.google.firebase.database.*

class FirebaseDataManager {
    private val database = FirebaseDatabase.getInstance()
    private val usersRef = database.getReference("users")
    
    fun saveUser(user: User) {
        usersRef.child(user.id.toString()).setValue(user)
    }
    
    fun observeUser(id: Int, listener: ValueEventListener) {
        usersRef.child(id.toString()).addValueEventListener(listener)
    }
}
```

## キャッシュ戦略

### ローカルキャッシュ

```swift
// 画像キャッシュ
import Kingfisher

class ImageCacheManager {
    static let shared = ImageCacheManager()
    
    private let cache = ImageCache.default
    
    init() {
        // キャッシュサイズの設定（100MB）
        cache.diskStorage.config.sizeLimit = 100 * 1024 * 1024
        cache.memoryStorage.config.totalCostLimit = 50 * 1024 * 1024
    }
    
    func loadImage(url: URL, into imageView: UIImageView) {
        imageView.kf.setImage(with: url)
    }
    
    func clearCache() {
        cache.clearMemoryCache()
        cache.clearDiskCache()
    }
}
```

```kotlin
// Android - Glide
import com.bumptech.glide.Glide
import com.bumptech.glide.load.engine.DiskCacheStrategy

class ImageCacheManager {
    fun loadImage(url: String, imageView: ImageView) {
        Glide.with(context)
            .load(url)
            .diskCacheStrategy(DiskCacheStrategy.ALL)
            .into(imageView)
    }
    
    fun clearCache(context: Context) {
        Glide.get(context).clearMemory()
        Thread {
            Glide.get(context).clearDiskCache()
        }.start()
    }
}
```

## オーケストレーション

### BaaS（Backend as a Service）

```swift
// Firebase / AWS Amplify / Supabase
import Amplify

class BaaSManager {
    func configure() {
        do {
            try Amplify.add(plugin: AWSCognitoAuthPlugin())
            try Amplify.add(plugin: AWSAPIPlugin())
            try Amplify.configure()
        } catch {
            print("Amplify configuration error: \(error)")
        }
    }
    
    func queryUsers(completion: @escaping ([User]) -> Void) {
        Amplify.API.query(request: .list(User.self)) { result in
            switch result {
            case .success(let users):
                completion(users)
            case .failure(let error):
                print("Query error: \(error)")
            }
        }
    }
}
```

### REST/GraphQL API

```python
# GraphQL API（バックエンド）
from graphene import ObjectType, String, Int, List, Field
import graphene

class User(ObjectType):
    id = Int()
    email = String()
    username = String()

class Query(ObjectType):
    users = List(User)
    user = Field(User, id=Int(required=True))
    
    def resolve_users(self, info):
        return db.session.query(User).all()
    
    def resolve_user(self, info, id):
        return db.session.query(User).filter_by(id=id).first()

schema = graphene.Schema(query=Query)
```

```swift
// GraphQL クライアント（iOS）
import Apollo

class GraphQLClient {
    private let apollo = ApolloClient(url: URL(string: "https://api.example.com/graphql")!)
    
    func fetchUsers(completion: @escaping ([User]) -> Void) {
        apollo.fetch(query: UsersQuery()) { result in
            switch result {
            case .success(let graphQLResult):
                if let users = graphQLResult.data?.users {
                    completion(users)
                }
            case .failure(let error):
                print("GraphQL error: \(error)")
            }
        }
    }
}
```

## 実装例

### 完全なモバイルアプリ構成

```swift
// iOS - 完全な実装例
class AppDataManager {
    private let localDB: CoreDataStack
    private let apiClient: APIClient
    private let syncManager: DataSyncManager
    
    init() {
        localDB = CoreDataStack()
        apiClient = APIClient()
        syncManager = DataSyncManager(
            context: localDB.context,
            apiClient: apiClient
        )
        
        // アプリ起動時に同期
        syncManager.syncInBackground()
        
        // バックグラウンドでの定期的な同期
        NotificationCenter.default.addObserver(
            forName: UIApplication.didBecomeActiveNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.syncManager.syncInBackground()
        }
    }
    
    func getUser(id: Int, completion: @escaping (User?) -> Void) {
        // オフライン優先: まずローカルから取得
        if let user = localDB.getUser(id: id) {
            completion(user)
        }
        
        // バックグラウンドで最新データを取得
        apiClient.getUser(id: id) { result in
            switch result {
            case .success(let user):
                localDB.saveUser(user)
                completion(user)
            case .failure:
                // オフライン時はローカルデータを返す
                completion(localDB.getUser(id: id))
            }
        }
    }
}
```

## まとめ

### 重要なポイント

1. **オフライン優先**: ローカルデータベースを主要なデータソースとして使用
2. **効率的な同期**: 差分同期、バッチ処理、データ圧縮
3. **セキュアな認証**: トークンベース認証、セキュアストレージ
4. **UX最適化**: 即座のレスポンス、バックグラウンド同期
5. **コスト効率**: データ転送の最適化、キャッシング

### 次のステップ

- [リアルタイムアプリケーション](./06_realtime_apps.md) - リアルタイム同期が必要な場合
- [共通パターンとベストプラクティス](./08_common_patterns.md) - より高度なパターン
- [セキュリティベストプラクティス](./09_security_best_practices.md) - セキュリティの強化

### 推奨ツールとサービス

- **ローカルDB**: Core Data (iOS), Room (Android), Realm, SQLite
- **BaaS**: Firebase, AWS Amplify, Supabase, Backendless
- **API**: REST, GraphQL (Apollo, Relay)
- **同期**: CloudKit (iOS), Firebase Realtime Database
- **認証**: OAuth 2.0, JWT, Firebase Auth, AWS Cognito
- **画像キャッシュ**: Kingfisher (iOS), Glide (Android), SDWebImage

