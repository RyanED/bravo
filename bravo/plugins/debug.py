from zope.interface import implements

from bravo.ibravo import IConsoleCommand

from bravo.parameters import factory

class Meliae(object):

    implements(IConsoleCommand)

    def console_command(self, parameters):
        out = "".join(parameters)
        try:
            import meliae.scanner
            meliae.scanner.dump_all_objects(out)
        except ImportError:
            raise Exception("Couldn't import meliae!")
        except IOError:
            raise Exception("Couldn't save to file %s!" % parameters)

        return tuple()

    name = "dump-memory"
    aliases = tuple()
    usage = "<filename>"
    info = "Dump a JSON snapshot of memory usage using Meliae"

class Status(object):

    implements(IConsoleCommand)

    def console_command(self, parameters):
        protocol_count = len(factory.protocols)
        yield "%d protocols connected" % protocol_count

        for name, protocol in factory.protocols.iteritems():
            count = len(protocol.chunks)
            dirty = len([i for i in protocol.chunks.values() if i.dirty])
            yield "%s: %d chunks (%d dirty)" % (name, count, dirty)

        chunk_count = len(factory.world.chunk_cache)
        dirty = len(factory.world.dirty_chunk_cache)
        chunk_count += dirty
        yield "World cache: %d chunks (%d dirty)" % (chunk_count, dirty)

    name = "status"
    aliases = tuple()
    usage = ""
    info = "Print a quick summary of the server's status"

meliae = Meliae()
status = Status()
