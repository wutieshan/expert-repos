#include <map>
#include <mutex>
#include <shared_mutex>
#include <string>

class dns_entry
{
};

class dns_cache
{
public:
    dns_entry find_entry(const std::string &domain) const
    {
        // 读: 允许多个线程同时持有
        std::shared_lock lock(mutex_);
        auto it = entries_.find(domain);
        return it == entries_.end() ? dns_entry() : it->second;
    }

    void update_entry(const std::string &domain, const dns_entry &entry)
    {
        // 写: 同时只能由一个线程持有
        std::lock_guard lock(mutex_);
        entries_[domain] = entry;
    }

private:
    std::map<std::string, dns_entry> entries_;
    mutable std::shared_mutex mutex_;
};