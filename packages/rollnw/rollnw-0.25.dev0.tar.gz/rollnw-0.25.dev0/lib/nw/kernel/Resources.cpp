#include "Resources.hpp"

#include "../formats/Ini.hpp"
#include "../formats/palette_textures.hpp"
#include "../util/game_install.hpp"
#include "../util/platform.hpp"
#include "../util/templates.hpp"
#include "Kernel.hpp"
#include "Strings.hpp"

#include <filesystem>
#include <memory>

namespace fs = std::filesystem;
using namespace std::literals;

namespace nw::kernel {

inline const Container* get_container(const LocatorVariant& var)
{
    if (std::holds_alternative<Container*>(var)) {
        return std::get<Container*>(var);
    } else {
        return std::get<unique_container>(var).get();
    }
}

inline Container* resolve_container(const std::filesystem::path& p, const std::string& name)
{
    if (fs::is_directory(p / name)) {
        return new Directory{p / name};
    } else if (fs::exists(p / (name + ".hak"))) {
        return new Erf{p / (name + ".hak")};
    } else if (fs::exists(p / (name + ".erf"))) {
        return new Erf{p / (name + ".erf")};
    } else if (fs::exists(p / (name + ".zip"))) {
        return new Zip{p / (name + ".zip")};
    }
    return nullptr;
}

Resources::Resources(const Resources* parent)
    : parent_(parent)
{
}

void Resources::initialize()
{
    LOG_F(INFO, "kernel: initializing resource system");

    if (config().options().include_user) {
        ambient_user_ = Directory{config().user_path() / "ambient"};
        dmvault_user_ = Directory{config().user_path() / "dmvault"};
        localvault_user_ = Directory{config().user_path() / "localvault"};
        music_user_ = Directory{config().user_path() / "music"};
        override_user_ = Directory{config().user_path() / "override"};
        portraits_user_ = Directory{config().user_path() / "portraits"};
        servervault_user_ = Directory{config().user_path() / "servervault"};
    }

    if (config().options().include_user) {
        if (config().version() == GameVersion::vEE) {
            if (config().options().include_nwsync) {
                nwsync_ = NWSync{config().user_path() / "nwsync"};
            }
            development_ = Directory{config().user_path() / "development"};
        }
    }

    if (config().options().include_user) {
        if (fs::exists(config().user_path() / "userpatch.ini")) {
            Ini user_patch{config().user_path() / "userpatch.ini"};
            if (user_patch.valid()) {
                int i = 0;
                std::string file;
                while (user_patch.get_to(fmt::format("Patch/PatchFile{:03d}", i++), file)) {
                    auto c = resolve_container(config().user_path() / "patch", file);
                    if (c) {
                        patches_.emplace_back(c);
                    }
                }
            }
        }
    }

    if (config().options().include_install) {
        texture_packs_.reserve(4);
        if (config().version() == GameVersion::vEE) {
            ambient_install_ = Directory{config().install_path() / "data/amb/"};
            dmvault_install_ = Directory{config().install_path() / "data/dmv/"};
            localvault_install_ = Directory{config().install_path() / "data/lcv/"};
            music_install_ = Directory{config().install_path() / "data/mus"};
            override_install_ = Directory{config().install_path() / "ovr"};
            portraits_install_ = Directory{config().install_path() / "data/prt/"};

            texture_packs_.emplace_back(config().install_path() / "data/txpk/xp2_tex_tpa.erf");
            texture_packs_.emplace_back(config().install_path() / "data/txpk/xp1_tex_tpa.erf");
            texture_packs_.emplace_back(config().install_path() / "data/txpk/textures_tpa.erf");
            texture_packs_.emplace_back(config().install_path() / "data/txpk/tiles_tpa.erf");

            keys_.reserve(2);
            auto lang = strings().global_language();
            if (lang != LanguageID::english) {
                auto shortcode = Language::to_string(lang);
                keys_.emplace_back(config().install_path() / "lang" / shortcode / "data" / "nwn_base_loc.key");
            }
            keys_.emplace_back(config().install_path() / "data/nwn_base.key");
        } else {
            texture_packs_.emplace_back(config().install_path() / "texturepacks/xp2_tex_tpa.erf");
            texture_packs_.emplace_back(config().install_path() / "texturepacks/xp1_tex_tpa.erf");
            texture_packs_.emplace_back(config().install_path() / "texturepacks/textures_tpa.erf");
            texture_packs_.emplace_back(config().install_path() / "texturepacks/tiles_tpa.erf");

            keys_.reserve(8);
            keys_.emplace_back(config().install_path() / "xp3patch.key");
            keys_.emplace_back(config().install_path() / "xp3.key");
            keys_.emplace_back(config().install_path() / "xp2patch.key");
            keys_.emplace_back(config().install_path() / "xp2.key");
            keys_.emplace_back(config().install_path() / "xp1patch.key");
            keys_.emplace_back(config().install_path() / "xp1.key");
            keys_.emplace_back(config().install_path() / "patch.key");
            keys_.emplace_back(config().install_path() / "chitin.key");
        }
    }
    update_container_search();
    load_palette_textures();
}

bool Resources::load_module(std::filesystem::path path, std::string_view manifest)
{
    LOG_F(INFO, "resman: loading module container: {}", path);

    if (fs::is_directory(path) && fs::exists(path / "module.ifo")) {
        module_ = std::make_unique<Directory>(path);
    } else if (fs::exists(path) && string::icmp(path_to_string(path.extension()), ".mod")) {
        module_ = std::make_unique<Erf>(path);
    } else if (fs::exists(path) && string::icmp(path_to_string(path.extension()), ".zip")) {
        module_ = std::make_unique<Zip>(path);
    }

    if (!module_ || !module_->valid()) {
        LOG_F(ERROR, "Failed to load module at '{}'", path);
        return false;
    }

    module_path_ = std::move(path);
    nwsync_manifest_ = nwsync_.get(manifest);
    update_container_search();
    return true;
}

void Resources::load_module_haks(const std::vector<std::string>& haks)
{
    // [TODO] - Change to resolve container
    for (const auto& h : haks) {
        haks_.emplace_back(config().user_path() / "hak" / (h + ".hak"));
    }
}

void Resources::unload_module()
{
    LOG_F(INFO, "resman: unloading module container: {}", module_path_);
    module_path_.clear();
    nwsync_manifest_ = nullptr;
    haks_.clear();
    module_.reset();
    update_container_search();
}

bool Resources::add_container(Container* container, bool take_ownership)
{
    if (!container || !container->valid()) {
        return false;
    }
    for (auto& [cont, type, user] : search_) {
        if (cont->path() == container->path()) {
            return false;
        }
    }

    if (take_ownership) {
        custom_.emplace_back(unique_container{container});
    } else {
        custom_.push_back(container);
    }

    update_container_search();

    return true;
}

void Resources::clear_containers()
{
    custom_.clear();
    update_container_search();
}

bool Resources::contains(Resource res) const
{
    for (auto [cont, type, user] : search_) {
        if (type != ResourceType::invalid && !ResourceType::check_category(type, res.type)) {
            continue;
        }
        if (cont->contains(res)) { return true; }
    }

    if (parent_ && parent_->contains(res)) {
        return true;
    }

    return false;
}

ResourceData Resources::demand(Resource res) const
{
    ResourceData result;
    for (auto [cont, type, user] : search_) {
        if (type != ResourceType::invalid && !ResourceType::check_category(type, res.type)) {
            continue;
        }
        result = cont->demand(res);
        if (result.bytes.size()) {
            break;
        }
    }

    if (result.bytes.size() == 0 && parent_) { result = parent_->demand(res); }

    if (result.bytes.size() == 0) {
        LOG_F(WARNING, "Failed to find '{}'", res.filename());
    }
    return result;
}

ResourceData Resources::demand_any(Resref resref, std::initializer_list<ResourceType::type> restypes) const
{
    ResourceData result;
    for (auto [cont, type, user] : search_) {
        for (auto rt : restypes) {
            Resource res{resref, rt};
            if (type != ResourceType::invalid && !ResourceType::check_category(type, res.type)) {
                continue;
            }
            result = cont->demand(res);
            if (result.bytes.size()) {
                return result;
            }
        }
    }
    return parent_ ? parent_->demand_any(resref, restypes) : ResourceData{};
}

ResourceData Resources::demand_in_order(Resref resref, std::initializer_list<ResourceType::type> restypes) const
{
    ResourceData result;
    for (auto rt : restypes) {
        Resource res{resref, rt};
        for (auto [cont, type, user] : search_) {
            if (type != ResourceType::invalid && !ResourceType::check_category(type, res.type)) {
                continue;
            }
            result = cont->demand(res);
            if (result.bytes.size()) {
                return result;
            }
        }
    }
    return parent_ ? parent_->demand_in_order(resref, restypes) : ResourceData{};
}

ResourceData Resources::demand_server_vault(std::string_view cdkey, std::string_view resref)
{
    ResourceData result;
    auto vault_path = config().user_path() / "servervault";
    if (!fs::exists(vault_path)) { return result; }

    vault_path /= cdkey;
    if (!fs::exists(vault_path)) { return result; }

    Resource res{resref, ResourceType::bic};
    vault_path /= res.filename();
    if (!fs::exists(vault_path)) { return result; }
    result = ResourceData::from_file(vault_path);

    return result;
}

int Resources::extract(const std::regex& pattern, const std::filesystem::path& output) const
{
    int result = 0;
    for (auto [cont, type, user] : reverse(search_)) {
        result += cont->extract(pattern, output);
    }

    if (parent_) {
        result += parent_->extract(pattern, output);
    }
    return result;
}

size_t Resources::size() const
{
    size_t result = 0;
    for (auto [cont, type, user] : search_) {
        result += cont->size();
    }
    return result;
}

ResourceDescriptor Resources::stat(const Resource& res) const
{
    ResourceDescriptor rd;
    for (auto [cont, type, user] : search_) {
        rd = cont->stat(res);
        if (rd) {
            break;
        }
    }
    return rd;
}

void Resources::visit(std::function<void(const Resource&)> callback) const noexcept
{
    for (auto [cont, type, user] : search_) {
        cont->visit(callback);
    }
}

void Resources::load_palette_textures()
{
    // [TODO]: Fix all this with a image/texture cache at some point
    palette_textures_[plt_layer_skin] = std::make_unique<Image>(demand(Resource("pal_skin01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_hair] = std::make_unique<Image>(demand(Resource("pal_hair01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_metal1] = std::make_unique<Image>(demand(Resource("pal_armor01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_metal2] = std::make_unique<Image>(demand(Resource("pal_armor02"sv, ResourceType::tga)));
    palette_textures_[plt_layer_cloth1] = std::make_unique<Image>(demand(Resource("pal_cloth01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_cloth2] = std::make_unique<Image>(demand(Resource("pal_cloth01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_leather1] = std::make_unique<Image>(demand(Resource("pal_leath01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_leather2] = std::make_unique<Image>(demand(Resource("pal_leath01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_tattoo1] = std::make_unique<Image>(demand(Resource("pal_tattoo01"sv, ResourceType::tga)));
    palette_textures_[plt_layer_tattoo2] = std::make_unique<Image>(demand(Resource("pal_tattoo01"sv, ResourceType::tga)));
}

Image* Resources::palette_texture(PltLayer layer)
{
    if (palette_textures_[layer] && palette_textures_[layer]->valid()) {
        return palette_textures_[layer].get();
    }
    ResourceData data;
    data.name = Resource{"<plttex>"sv, ResourceType::tga};
    switch (layer) {
    default:
        return nullptr;
    case plt_layer_skin:
        data.bytes.append(pal_skin01_tga, pal_skin01_tga_len);
        break;
    case plt_layer_hair:
        data.bytes.append(pal_hair01_tga, pal_hair01_tga_len);
        break;
    case plt_layer_metal1:
        data.bytes.append(pal_armor01_tga, pal_armor01_tga_len);
        break;
    case plt_layer_metal2:
        data.bytes.append(pal_armor02_tga, pal_armor02_tga_len);
        break;
    case plt_layer_cloth1:
    case plt_layer_cloth2:
        data.bytes.append(pal_armor02_tga, pal_armor02_tga_len);
        break;
    case plt_layer_leather1:
    case plt_layer_leather2:
        data.bytes.append(pal_armor02_tga, pal_armor02_tga_len);
        break;
    case plt_layer_tattoo1:
    case plt_layer_tattoo2:
        data.bytes.append(pal_armor02_tga, pal_armor02_tga_len);
        break;
    }

    palette_textures_[layer] = std::make_unique<Image>(std::move(data));

    return palette_textures_[layer]->valid() ? palette_textures_[layer].get() : nullptr;
}

void Resources::update_container_search()
{
    if (search_.size()) {
        search_.clear();
    }

    auto push_container = [this](const Container* c, ResourceType::type cat, bool user) {
        if (c && c->valid()) {
            search_.emplace_back(c, cat, user);
        }
    };

    for (auto& c : custom_) {
        push_container(get_container(c), ResourceType::invalid, true);
    }

    push_container(&portraits_user_, ResourceType::texture, true);
    push_container(&portraits_install_, ResourceType::texture, false);

    // Vault
    // push_container(vault_user_, ResourceType::player, true);

    push_container(&development_, ResourceType::invalid, true);

    push_container(nwsync_manifest_, ResourceType::invalid, true);

    for (const auto& c : haks_) {
        push_container(&c, ResourceType::invalid, false);
    }

    push_container(module_.get(), ResourceType::invalid, true);

    push_container(&override_user_, ResourceType::invalid, true);
    push_container(&override_install_, ResourceType::invalid, false);

    push_container(&ambient_user_, ResourceType::sound, true);
    push_container(&music_user_, ResourceType::sound, true);
    push_container(&ambient_install_, ResourceType::sound, false);
    push_container(&music_install_, ResourceType::sound, false);

    for (auto& c : patches_) {
        push_container(c.get(), ResourceType::invalid, false);
    }

    for (auto& c : texture_packs_) {
        push_container(&c, ResourceType::texture, false);
    }

    for (auto& c : keys_) {
        push_container(&c, ResourceType::invalid, false);
    }
}

} // namespace nw::kernel
