# frozen_string_literal: true

require "nokogiri"
require "pathname"
require "set"
require "uri"

site_root = Pathname.new(ARGV.fetch(0, "_site")).expand_path
abort "Site directory not found: #{site_root}" unless site_root.directory?

html_paths = Dir.glob(site_root.join("**", "*.html").to_s).sort
documents = {}
ids_by_path = {}
errors = []
reference_count = 0

html_paths.each do |path|
  document = Nokogiri::HTML(File.read(path))
  expanded_path = Pathname.new(path).expand_path.to_s
  documents[expanded_path] = document
  ids_by_path[expanded_path] = document.css("[id]").map { |node| node["id"] }.to_set

  relative_path = Pathname.new(path).relative_path_from(site_root)
  h1_count = document.css("h1").length
  errors << "#{relative_path}: expected one h1, found #{h1_count}" unless h1_count == 1

  id_counts = document.css("[id]").each_with_object(Hash.new(0)) do |node, counts|
    counts[node["id"]] += 1
  end
  duplicate_ids = id_counts.select { |_id, count| count > 1 }
  duplicate_ids.each_key do |id|
    errors << "#{relative_path}: duplicate id ##{id}"
  end

  document.css("img").each do |image|
    if !image.key?("alt") || image["alt"].strip.empty?
      errors << "#{relative_path}: image is missing descriptive alt text (#{image['src']})"
    end
  end
end

def local_target(site_root, source_path, reference)
  return nil if reference.nil? || reference.empty? || reference.start_with?("//")

  uri = URI.parse(reference)
  return nil if uri.scheme || uri.host

  decoded_path = URI::DEFAULT_PARSER.unescape(uri.path.to_s)
  candidate = if decoded_path.empty?
                source_path
              elsif decoded_path.start_with?("/")
                site_root.join(decoded_path.delete_prefix("/"))
              else
                source_path.dirname.join(decoded_path)
              end

  candidate = candidate.cleanpath
  candidates = [candidate]
  candidates << candidate.join("index.html")
  candidates << Pathname.new("#{candidate}.html") unless candidate.extname == ".html"

  target = candidates.find(&:file?)
  [target, uri.fragment]
rescue URI::InvalidURIError
  :invalid
end

documents.each do |path, document|
  source_path = Pathname.new(path)
  relative_path = source_path.relative_path_from(site_root)

  document.css("a[href], img[src], script[src], link[href]").each do |node|
    attribute = node.key?("href") ? "href" : "src"
    reference = node[attribute]
    next if reference.start_with?("mailto:", "tel:", "javascript:", "data:")

    result = local_target(site_root, source_path, reference)
    next if result.nil?

    reference_count += 1
    if result == :invalid
      errors << "#{relative_path}: invalid URL #{reference.inspect}"
      next
    end

    target, fragment = result
    unless target
      errors << "#{relative_path}: missing local target #{reference.inspect}"
      next
    end

    next if fragment.nil? || fragment.empty? || target.extname != ".html"

    target_path = target.expand_path.to_s
    target_ids = ids_by_path[target_path]
    unless target_ids&.include?(URI::DEFAULT_PARSER.unescape(fragment))
      errors << "#{relative_path}: missing fragment ##{fragment} in #{reference.inspect}"
    end
  end
end

if errors.any?
  warn errors.join("\n")
  abort "Site check failed with #{errors.length} error(s)."
end

puts "Checked #{html_paths.length} HTML files and #{reference_count} local references."
