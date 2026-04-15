# frozen_string_literal: true

# Jekyll plugin: stamp each page with git-derived date_published and date_modified.
#
# Why a plugin and not manual frontmatter:
#   - Eliminates drift between visible "Last updated: ..." strings and reality.
#   - `dateModified` in JSON-LD is Google's freshness signal; hand-editing 31
#     pages on every content change would guarantee staleness.
#
# Behavior:
#   - `page.date_published`: first commit that touched the source file.
#   - `page.date_modified`:  most recent commit that touched the source file.
#   - If the file is not yet committed (or git is unavailable), falls back to
#     the file's filesystem mtime so local builds still validate.
#   - `_data/site_meta.yml` -> `date_published_overrides` wins over git.
#
# Implemented as a Generator (runs in :site, :post_read phase) so the dates
# are present on page.data *before* any page renders — this matters because
# sitemap.xml iterates site.html_pages and expects lastmod on every entry.

require "date"
require "open3"

module UsdthubGitDates
  class Generator < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      cache = {}

      (site.pages + site.documents).each do |page|
        next unless page.respond_to?(:path) && page.path

        abs_path =
          if page.path.start_with?("/")
            page.path
          else
            File.join(site.source, page.path)
          end
        next unless File.file?(abs_path)

        cache[abs_path] ||= dates_for(abs_path, site.source)
        dates = cache[abs_path]

        overrides = (site.data["site_meta"] && site.data["site_meta"]["date_published_overrides"]) || {}
        permalink = page.data["permalink"] || page.url
        if overrides[permalink]
          begin
            dates = dates.merge(published: DateTime.parse("#{overrides[permalink]}T00:00:00Z"))
          rescue StandardError
            # keep git-derived date
          end
        end

        if dates[:published] && dates[:modified] && dates[:published] > dates[:modified]
          dates = dates.merge(modified: dates[:published])
        end

        page.data["date_published"] ||= dates[:published]
        page.data["date_modified"]  ||= dates[:modified]
      end
    end

    private

    def dates_for(abs_path, source)
      rel = abs_path.sub(%r{\A#{Regexp.escape(source)}/}, "")
      created, modified = git_dates(rel, source)
      created ||= file_mtime(abs_path)
      modified ||= created
      { published: created, modified: modified }
    end

    def git_dates(rel_path, cwd)
      out, status = Open3.capture2(
        "git", "log", "--follow", "--format=%aI", "--", rel_path,
        chdir: cwd
      )
      return [nil, nil] unless status.success?
      lines = out.each_line.map(&:strip).reject(&:empty?)
      return [nil, nil] if lines.empty?
      [parse_iso(lines.last), parse_iso(lines.first)]
    rescue StandardError
      [nil, nil]
    end

    def parse_iso(s)
      DateTime.iso8601(s)
    rescue StandardError
      nil
    end

    def file_mtime(abs_path)
      DateTime.parse(File.mtime(abs_path).iso8601)
    rescue StandardError
      DateTime.now
    end
  end
end
